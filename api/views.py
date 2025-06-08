from datetime import datetime

import requests
from django.utils import timezone
from geopy.geocoders import Nominatim
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api import consts
from api.exeptions import LocationError
from api.serializers import (
    ForecastQueryParamsSerializer,
    ForecastReadSerializer,
    ForecastWriteSerializer,
)
from weather.models import Forecast


class BaseWeatherMixin:
    """Mixin to work with weather forecast through open-meteo."""

    @staticmethod
    def get_forecast(city_name: str, days_count: int):
        """
        Fetches daily weather forecast from Open-Meteo API.

        Args:
            city_name (str): Name of the city to fetch forecast for.
            days_count (int): Number of forecast days (max 16 supported).

        Raises:
            LocationError: If the city cannot be geocoded.

        Returns:
            Response: HTTP response object from Open-Meteo API.
        """
        geolocator = Nominatim(user_agent='weather_api')

        location = geolocator.geocode(city_name)
        if not location:
            raise LocationError

        lat, lon = location.latitude, location.longitude

        response = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params={
                'latitude': lat,
                'longitude': lon,
                'daily': 'temperature_2m_min,temperature_2m_max',
                'timezone': 'auto',
                'forecast_days': days_count,
            },
        )

        return response

    @staticmethod
    def parse_weather_response(response: Response):
        """
        Parses weather API response and handles possible errors.

        Args:
            response (Response): HTTP response object from the weather API.

        Returns:
            Tuple[dict | None, Response | None]: Parsed JSON data and None on
            success,
            or None and DRF Response on failure.
        """
        if response.status_code != status.HTTP_200_OK:
            return None, Response(response.json(), status=response.status_code)

        try:
            data = response.json()
            return data, None
        except Exception:
            return None, Response(
                {'message': 'Ошибка при парсинге данных с погодного API'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_validated_forecast(self, city: str, days_count: int):
        """
        Validates city and fetches weather data from Open-Meteo API.

        Args:
            city (str): City name.
            days_count (int): Number of forecast days.

        Returns:
            Tuple[dict | None, Response | None]: Parsed forecast data or error
            response.
        """
        try:
            response = self.get_forecast(city, days_count)
        except LocationError:
            return None, Response(
                {'message': 'Локация не найдена.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        return self.parse_weather_response(response)


class CurrentWeatherView(BaseWeatherMixin, APIView):
    """View for precessing requests for current weather."""

    def get(self, request):
        city = request.query_params.get('city')

        if not city:
            return Response(
                {'message': 'Не передан обязательный параметр city.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data, error_response = self.get_validated_forecast(city, 1)

        if error_response:
            return error_response

        min_temp = data['daily']['temperature_2m_min'][0]
        max_temp = data['daily']['temperature_2m_max'][0]

        return Response(
            data={
                'min_temperature': min_temp,
                'max_temperature': max_temp,
            },
            status=status.HTTP_200_OK,
        )


class ForecastWeatherView(BaseWeatherMixin, APIView):
    """View for precessing requests for forecast weather."""

    def get(self, request):
        city = request.query_params.get('city')
        date = request.query_params.get('date')
        forecast_response = Forecast.objects.filter(
            name=city, date=datetime.strptime(date, consts.DATE_FORMAT)
        )

        if forecast_response.exists():
            return Response(
                data=ForecastReadSerializer(forecast_response.first()).data,
                status=status.HTTP_200_OK,
            )

        serializer = ForecastQueryParamsSerializer(
            data={'city': city, 'date': date}
        )
        serializer.is_valid(raise_exception=True)
        diff = (serializer.validated_data['date'] - timezone.now().date()).days
        data, error_response = self.get_validated_forecast(city, 11)

        if error_response:
            return error_response

        min_temp = data['daily']['temperature_2m_min'][diff]
        max_temp = data['daily']['temperature_2m_max'][diff]

        return Response(
            data={
                'min_temperature': min_temp,
                'max_temperature': max_temp,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = ForecastWriteSerializer(
            data={
                'name': request.query_params['city'],
                'date': request.query_params['date'],
                'min_temperature': request.query_params['min_temperature'],
                'max_temperature': request.query_params['max_temperature'],
            },
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

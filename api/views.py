import requests
from config import config
from rest_framework import status
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.views import APIView


class CurrentWeatherView(APIView):

    def get(self, request):
        city = request.query_params.get('city')

        if not city:
            raise ValidationError(
                detail={'message': 'Не передан обязательный параметр city.'}
            )

        response = requests.get(
            config.open_weather.url,
            params={
                'q': city,
                'appid': config.open_weather.api_key,
                'units': 'metric',
                'lang': 'ru',
            },
        )

        response_data = response.json()
        if not response.status_code == status.HTTP_200_OK:
            return Response(data=response_data, status=response.status_code)

        return Response(
            data={
                'min_temperature': response_data['main']['temp_min'],
                'max_temperature': response_data['main']['temp_max'],
            },
            status=status.HTTP_200_OK,
        )

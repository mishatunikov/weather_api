from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from api import consts
from weather.models import Forecast


class DateSerializer(serializers.Serializer):
    """Serializer with date field."""

    date = serializers.DateField(
        required=True,
        format=consts.DATE_FORMAT,
        input_formats=[consts.DATE_FORMAT],
    )

    def validate_date(self, value):
        if value < timezone.now().date():
            raise ValidationError(
                detail={'message': 'The date cannot be in the past.'}
            )

        if value - timezone.now().date() > timedelta(10):
            raise ValidationError(
                detail={
                    'message': 'The date cannot be more than 10 days in the '
                    'future.'
                }
            )

        return value


class ForecastQueryParamsSerializer(DateSerializer):
    """Serializer for validate forecast query param."""

    city = serializers.CharField(required=True)


class ForecastReadSerializer(serializers.ModelSerializer):
    """Serializer for representation data of the Forecast Model."""

    class Meta:
        model = Forecast
        fields = ('min_temperature', 'max_temperature')


class ForecastWriteSerializer(DateSerializer, serializers.ModelSerializer):
    """Serializer create instance of the Forecast Model."""

    class Meta:
        model = Forecast
        fields = ('city', 'date', 'min_temperature', 'max_temperature')
        validators = [
            UniqueTogetherValidator(
                queryset=Forecast.objects.all(),
                fields=('city', 'date')
            )
        ]

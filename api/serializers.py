from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import ValidationError

from api import consts


class ForecastGetSerializer(serializers.Serializer):
    city = serializers.CharField(required=True)
    date = serializers.DateField(
        required=True,
        format=consts.DATE_FORMAT,
        input_formats=[consts.DATE_FORMAT],
    )

    def validate_date(self, value):
        if value < timezone.now().date():
            raise ValidationError(
                detail={'message': 'Дата не может быть прошлом.'}
            )

        if value - timezone.now().date() > timedelta(10):
            raise ValidationError(
                detail={
                    'message': 'Дата не может быть в будущем больше, '
                    'чем на 10 дней.'
                }
            )

        return value


class ForecastCreateSerializer(serializers.ModelSerializer):
    pass

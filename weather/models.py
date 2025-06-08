from django.db import models

from weather import consts
from weather.validators import temperature_validators


class Forecast(models.Model):
    name = models.CharField(
        max_length=consts.MAX_NAME_LENGTH, verbose_name='название'
    )
    date = models.DateField(verbose_name='дата прогноза')
    min_temperature = models.FloatField(
        verbose_name='минимальная температура',
        validators=temperature_validators,
    )
    max_temperature = models.FloatField(
        verbose_name='максимальная температура',
        validators=temperature_validators,
    )

    class Meta:
        ordering = ('-date',)
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'date'), name='unique_weather_forecast'
            ),
        ]

    def __str__(self):
        return f'{self.name}|{self.date}'

from django.db import models

from weather import consts
from weather.validators import temperature_validators


class Forecast(models.Model):
    city = models.CharField(
        max_length=consts.MAX_NAME_LENGTH, verbose_name='name of location'
    )
    date = models.DateField(verbose_name='date')
    min_temperature = models.FloatField(
        verbose_name='minimal temperature',
        validators=temperature_validators,
    )
    max_temperature = models.FloatField(
        verbose_name='maximum temperature',
        validators=temperature_validators,
    )

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return f'{self.city}|{self.date}'

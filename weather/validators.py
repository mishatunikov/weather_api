from django.core.validators import MaxValueValidator, MinValueValidator

from weather import consts

temperature_validators = [
    MinValueValidator(consts.MIN_TEMP),
    MaxValueValidator(consts.MAX_TEMP),
]

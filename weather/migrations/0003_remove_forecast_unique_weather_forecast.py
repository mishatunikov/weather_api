# Generated by Django 4.2 on 2025-06-08 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_rename_name_forecast_city'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='forecast',
            name='unique_weather_forecast',
        ),
    ]

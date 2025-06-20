from django.contrib import admin
from django.urls import include, path

from api.views import CurrentWeatherView, ForecastWeatherView

urlpatterns = [
    path('weather/current/', CurrentWeatherView.as_view()),
    path('weather/forecast/', ForecastWeatherView.as_view()),
]

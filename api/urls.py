from api.views import CurrentWeatherView, ForecastWeatherView
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('weather/current/', CurrentWeatherView.as_view()),
    path('weather/forcast/', ForecastWeatherView.as_view()),
]

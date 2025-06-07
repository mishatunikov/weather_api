from api.views import CurrentWeatherView
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('weather/current/', CurrentWeatherView.as_view()),
]

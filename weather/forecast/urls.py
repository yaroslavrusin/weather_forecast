from django.urls import path

from .views import SearchWeatherCity

urlpatterns = [
    path('', SearchWeatherCity.as_view(), name='main'),
]

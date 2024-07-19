from django.urls import path, include
from rest_framework import routers

from .views import SearchWeatherCity, ViewWeatherCity, CountCityToQueryView

router = routers.DefaultRouter()
router.register(r'api', CountCityToQueryView)

urlpatterns = [
    path('api/count/city', CountCityToQueryView.as_view()),
    path('weather/', ViewWeatherCity.as_view(), name='weather_city'),
    path('', SearchWeatherCity.as_view(), name='main')

]

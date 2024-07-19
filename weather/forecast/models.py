from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models

from . import utils


# Create your models here.

class City(models.Model):
    name = models.CharField(
        max_length=250,
        unique=True,
        db_index=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def get_weather_forecast(self):
        return utils.get_weather_forecast(
            self.latitude,
            self.longitude,
            datetime.now(),
            datetime.now() + timedelta(days=1)
        )

    def __str__(self):
        return self.name


class QueryHistory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    city_id = models.ForeignKey(City, on_delete=models.CASCADE, related_name='history')
    created_date = models.DateTimeField(auto_now_add=True)

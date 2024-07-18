from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=250, unique=True, db_index=True)
    latitude = models.FloatField()
    longitude = models.FloatField()


class QueryHistory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    city_id = models.ForeignKey(City, on_delete=models.CASCADE, related_name='history')
    created_date = models.DateTimeField(auto_now_add=True)

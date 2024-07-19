from datetime import datetime

import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

URL = 'https://api.open-meteo.com/v1/forecast'
CACHE_SESSION = requests_cache.CachedSession('../cache_for_requests/.cache', expire_after=3600)
RETRY_SESSION = retry(CACHE_SESSION, retries=5, backoff_factor=0.2)
OPENMETEO = openmeteo_requests.Client(session=RETRY_SESSION)


def get_weather_forecast(
        latitude: float,
        longitude: float,
        start_date: datetime,
        end_date: datetime) -> pd.DataFrame:
    """Запрашиваем данные с open-meteo.com о температуре за указанный период"""
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': ['temperature_2m'],
        'timezone': 'UTC',
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    }
    responses = OPENMETEO.weather_api(URL, params=params)
    response = responses[0]
    hourly = response.Hourly()
    hourly_temperature_2m = map(int, hourly.Variables(0).ValuesAsNumpy())
    hourly_data = {'date': pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit='s', utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit='s', utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive='left'
    ), 'temperature_2m': hourly_temperature_2m}
    hourly_dataframe = pd.DataFrame(data=hourly_data)
    return hourly_dataframe

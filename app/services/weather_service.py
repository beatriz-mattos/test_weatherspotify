from flask_caching import Cache
import requests
from app.config import Config

cache = Cache()

@cache.cached(timeout=300, key_prefix='weather')
def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={Config.OPENWEATHERMAP_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    if response.status_code != 200:
        raise Exception(f"Error fetching weather data: {data}")
    return data

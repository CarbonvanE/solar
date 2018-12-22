""" All functions necessary to create and return views """
from datetime import datetime
import json
import requests

from django.core.cache import cache


def is_it_night(lat, lng):
    """ Checks if it is currently night """
    url = f'http://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0'
    response = requests.get(url)
    data = json.loads(response.content)['results']

    utc_time = datetime.utcnow()
    sunrise = datetime.strptime(data['sunrise'], '%Y-%m-%dT%H:%M:%S+00:00')
    sunset = datetime.strptime(data['sunset'], '%Y-%m-%dT%H:%M:%S+00:00')
    if  sunrise < utc_time < sunset:
        return False
    return True


def get_current_power(site_id, api_key):
    """ Checks what current power output is of the solar panels """
    url = f'https://monitoringapi.solaredge.com/site/{site_id}/overview?api_key={api_key}'
    response = requests.get(url)
    data = json.loads(response.content)
    current_power = data['overview']['currentPower']['power']
    return current_power


def what_is_the_weather(site_id, api_key, lat, lng):
    """ checks what the weather is and returns a FontAwesome class """
    weather_symbol = cache.get('weather_symbol')
    if weather_symbol is not None:
        return weather_symbol

    is_night = is_it_night(lat, lng)
    current_power = get_current_power(site_id, api_key)
    if is_night:
        weather_symbol = 'fa-moon'
    elif current_power > 1000:
        weather_symbol = 'fa-sun'
    elif current_power > 100:
        weather_symbol = 'fa-cloud-sun'
    elif current_power >= 0:
        weather_symbol = 'fa-cloud'
    else:
        weather_symbol = 'fa-exclamation-triangle'
    cache.set('weather_symbol', weather_symbol, 5 * 60)
    return weather_symbol

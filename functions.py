""" All functions necessary to create and return views """
from datetime import datetime
from math import floor, ceil
from statistics import mean
import json
import requests

from django.core.cache import cache

def get_start_and_end_date(site_id, api_key):
    """ Returns the start and the end date of the data in SolarEdge's database """
    url = f'https://monitoringapi.solaredge.com/site/{site_id}/dataPeriod?api_key={api_key}'
    response = requests.get(url)
    data = json.loads(response.content)
    start_date = data['dataPeriod']['startDate']
    end_date = data['dataPeriod']['endDate']
    return(start_date, end_date)


def get_averages(input_list, avg_range):
    new_list = []
    for index, item in enumerate(input_list):
        start_index = index - floor(avg_range / 2) if index - floor(avg_range / 2) >= 0 else 0
        end_index = index + ceil(avg_range / 2) if  index + ceil(avg_range / 2) <= len(input_list) else len(input_list)
        all_values_in_range = []
        for i in input_list[start_index: end_index]:
            all_values_in_range.append(i[1])
        average_value = round(mean(all_values_in_range), 1)
        new_list.append([item[0], average_value])
    return new_list


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

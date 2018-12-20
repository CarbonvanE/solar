from datetime import datetime
import json
import requests


def is_it_night(lat, lng):
    """ Checks if it is currently night """
    url = f'http://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&formatted=0'
    response = requests.get(url)
    data = json.loads(response.content)['results']

    time = datetime.utcnow()
    sunrise = datetime.strptime(data['sunrise'], '%Y-%m-%dT%H:%M:%S+00:00')
    sunset = datetime.strptime(data['sunset'], '%Y-%m-%dT%H:%M:%S+00:00')
    if  sunrise < time < sunset:
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
    if is_it_night(lat, lng):
        return 'fa-moon'
    current_power = get_current_power(site_id, api_key)
    if current_power > 1000:
        return 'fa-sun'
    if current_power > 100:
        return 'fa-cloud-sun'
    if current_power >= 0:
        return 'fa-cloud'
    return 'fa-exclamation-triangle'

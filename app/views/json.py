""" Handles all AJAX requests """

from datetime import datetime, timedelta
import pytz
import json
import requests

from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from functions import get_start_and_end_date, what_is_the_weather, get_averages


# Get the API key and site id
with open('solar/secrets.json', 'r') as f:
    DATA = json.load(f)
    API_KEY = DATA['SOLAREDGE']['API_KEY']
    SITE_ID = DATA['SOLAREDGE']['SITE_ID']
    TIME_ZONE = DATA['LOCATION']['TIME_ZONE']
    LAT = DATA['LOCATION']['LAT']
    LNG = DATA['LOCATION']['LNG']


def json_icon(request):
    """ Returns the relevant weather icon """
    icon = what_is_the_weather(SITE_ID, API_KEY, LAT, LNG)
    return JsonResponse({'icon': icon})


@login_required
def json_power_day(request):
    """ returns a json object with the power data of the last 24 hours """
    date_range = int(request.GET.get('range'))
    content = cache.get(f'power_day_{date_range}')
    if content is not None:
        return JsonResponse(content)
    start_time = (datetime.now(pytz.timezone(TIME_ZONE)) - timedelta(days=date_range)).strftime('%Y-%m-%d%%20%H:%M:%S')
    end_time = datetime.now(pytz.timezone(TIME_ZONE)).strftime('%Y-%m-%d%%20%H:%M:%S')
    time = f'startTime={start_time}&endTime={end_time}'
    url = f'https://monitoringapi.solaredge.com/site/{SITE_ID}/power?{time}&api_key={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)['power']['values']
        power_list = []
        for datum in data:
            date = datetime.strptime(datum['date'], '%Y-%m-%d %H:%M:%S')
            timestamp = int(date.strftime('%s')) * 1000
            power = round(datum['value'], 1) if datum['value'] is not None else 0.0
            power_list.append([timestamp, power])
        content = {
            'data': {
                'raw': {
                    'name': 'Power',
                    'data': power_list
                },
                'small_avg': {
                    'name': 'Hourly average',
                    'data': get_averages(power_list, 5)
                },
                'large_avg': {
                    'name': 'Three hour average',
                    'data': get_averages(power_list, 13)
                }
            },
            'success': True
        }
        cache.set(f'power_day_{date_range}', content, 5 * 60)
        return JsonResponse(content)
    return JsonResponse({'power': [], 'success': False})


@login_required
def json_energy_year_view(request):
    """ Returns a json object with all the energy data """
    content = cache.get('energy_year')
    if content is not None:
        return JsonResponse(content)
    start_date, end_date = get_start_and_end_date(SITE_ID, API_KEY)
    time = f'startDate={start_date}&endDate={end_date}'
    url = f'https://monitoringapi.solaredge.com/site/{SITE_ID}/energy?timeUnit=DAY&{time}&api_key={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)['energy']['values']
        energy_list = []
        for datum in data:
            date = datetime.strptime(datum['date'], '%Y-%m-%d %H:%M:%S').date()
            timestamp = int(date.strftime('%s')) * 1000
            energy = round(datum['value'] / 1000, 1) if datum['value'] is not None else 0.0
            energy_list.append([timestamp, energy])
        content = {
            'data': {
                'raw': {
                    'name': 'Daily generation',
                    'data': energy_list
                },
                'small_avg': {
                    'name': 'Weekly average',
                    'data': get_averages(energy_list, 7)
                },
                'large_avg': {
                    'name': 'Monthly average',
                    'data': get_averages(energy_list, 30)
                }
            },
            'success': True
        }
        cache.set('energy_year', content, 5 * 60)
        return JsonResponse(content)
    return JsonResponse({'energy': [], 'success': False})

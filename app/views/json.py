""" Handles all AJAX requests """

from datetime import datetime
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
    LAT = DATA['LOCATION']['LAT']
    LNG = DATA['LOCATION']['LNG']


def json_icon(request):
    """ Returns the relevant weather icon """
    icon = what_is_the_weather(SITE_ID, API_KEY, LAT, LNG)
    return JsonResponse({'icon': icon})


@login_required
def json_energy_day_view(request):
    """ Returns a json object with all the energy data """
    content = cache.get('energy_day')
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
            'energy': {
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
            'success': True}
        cache.set('energy_day', content, 5 * 60)
        return JsonResponse(content)
    return JsonResponse({'energy': [], 'success': False})

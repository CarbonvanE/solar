""" Handles the index page """

import json
import requests

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Get the API key and site id
with open('solar/secrets.json', 'r') as f:
    DATA = json.load(f)
    API_KEY = DATA['SOLAREDGE']['API_KEY']
    SITE_ID = DATA['SOLAREDGE']['SITE_ID']
    LAT = DATA['LOCATION']['LAT']
    LNG = DATA['LOCATION']['LNG']


@login_required
def index_view(request):
    """ Main page of the app """
    url = f'https://monitoringapi.solaredge.com/site/{SITE_ID}/overview?api_key={API_KEY}'
    response = requests.get(url)
    data = json.loads(response.content)['overview']
    context = {
        'last_updated': data['lastUpdateTime'],
        'energy_total': int(data['lifeTimeData']['energy'] / 1000),
        'energy_year': int(data['lastYearData']['energy'] / 1000),
        'energy_month': int(data['lastMonthData']['energy'] / 1000),
        'energy_day': round(data['lastDayData']['energy'] / 1000, 1),
        'current_power': int(data['currentPower']['power'])
    }
    print(data)
    return render(request, 'app/index.html', context)

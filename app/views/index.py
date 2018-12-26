""" Handles the index page """

import json
import requests

from decouple import config
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index_view(request):
    """ Main page of the app """
    url = f'https://monitoringapi.solaredge.com/site/{config("SITE_ID")}/overview?api_key={config("API_KEY")}'
    response = requests.get(url)
    data = json.loads(response.content)['overview']
    context = {
        'chart_url': '/json/power?range=1',
        'last_updated': data['lastUpdateTime'],
        'energy_total': int(data['lifeTimeData']['energy'] / 1000),
        'energy_year': int(data['lastYearData']['energy'] / 1000),
        'energy_month': int(data['lastMonthData']['energy'] / 1000),
        'energy_day': round(data['lastDayData']['energy'] / 1000, 1),
        'current_power': int(data['currentPower']['power'])
    }
    return render(request, 'app/index.html', context)

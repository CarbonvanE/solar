""" All view logic for the app """

from uuid import uuid4
from datetime import datetime, timedelta
import json
import requests

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from app.models import CustomUser, SuperSecretCode, EnergyPerDay

from functions import what_is_the_weather


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
        'weather': what_is_the_weather(SITE_ID, API_KEY, LAT, LNG),
        'last_updated': data['lastUpdateTime'],
        'energy_total': int(data['lifeTimeData']['energy'] / 1000),
        'energy_year': int(data['lastYearData']['energy'] / 1000),
        'energy_month': int(data['lastMonthData']['energy'] / 1000),
        'energy_day': round(data['lastDayData']['energy'] / 1000, 1),
        'current_power': int(data['currentPower']['power'])
    }
    print(data)
    return render(request, 'app/index.html', context)


def login_view(request):
    """ Login and register page """
    if request.method == 'POST':
        form = request.POST.dict()
        if 'super-secret-code' in form:
            message = ''
            code = SuperSecretCode.objects.filter(code=form['super-secret-code'])
            if form['password'] != form['password-check']:
                message = 'Passwords do not match.'
            elif CustomUser.objects.filter(email=form['email']).exists():
                message = 'This e-mail address already has an account.'
            elif not code.exists():
                message = 'This super secret code does not exist.'
            elif code.first().activated:
                message = 'This super secret code has already been used.'
            if message != '':
                return render(request, 'app/login.html', {'message': message, 'register': True})
            new_user = CustomUser.objects.create_user(email=form['email'],\
                first_name=form['first-name'],\
                password=form['password'],\
                username=uuid4())
            new_user.save()
            code.first().activated = True
            code.first().user = new_user
            code.first().save()
            user = authenticate(request, email=form['email'], password=form['password'])
            if user is None:
                message = "Something went wrong while creating your account. Please try again."
                return render(request, "app/login.html", {"message": message})
        else:
            user = authenticate(request, email=form['email'], password=form['password'])
            if user is None:
                return render(request, 'app/login.html', {'message': 'Invalid credentials.'})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    context = {
        'weather': what_is_the_weather(SITE_ID, API_KEY, LAT, LNG)
    }
    return render(request, 'app/login.html', context)


@login_required
def logout_view(request):
    """ Log the user out """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def password_reset_view(request):
    """ TODO: Create the password reset logic """
    context = {
        'weather': what_is_the_weather(SITE_ID, API_KEY, LAT, LNG),
        'message': 'Hahaha, too bad...'
    }
    return render(request, 'app/login.html', context)


@login_required
def user_settings_view(request):
    """ Returns the user settings page """
    first_name = request.user.first_name
    last_name = request.user.last_name
    email = request.user.email
    message = None
    if request.method == 'POST':
        user = CustomUser.objects.filter(email=request.user).first()
        code = request.POST['code']
        content = request.POST['content']
        if code == 'first name':
            user.first_name = content
            first_name = content
        elif code == 'last name':
            user.last_name = content
            last_name = content
        elif code == 'e-mail':
            user.email = content
            email = content
        elif code == 'password':
            user.set_password(content)
            login(request, user)
        message = code.capitalize() + ' has been succesfully updated!'
        user.save()
    context = {
        'weather': what_is_the_weather(SITE_ID, API_KEY, LAT, LNG),
        'message': message,
        'tab': 'settings',
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
    }
    return render(request, 'app/user_settings.html', context)


@login_required
def chart_settings_view(request):
    """ Returns the chart settings page """
    context = {
        'weather': what_is_the_weather(SITE_ID, API_KEY, LAT, LNG),
        'tab': 'settings'
    }
    return render(request, 'app/chart_settings.html', context)



@login_required
def json_energy_day_view(request):
    """ Returns a json object with all the energy data """
    time = 'startDate=2018-09-03&endDate=2018-12-22'
    url = f'https://monitoringapi.solaredge.com/site/{SITE_ID}/energy?timeUnit=DAY&{time}&api_key={API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)['energy']['values']
        energy_list = []
        for datum in data:
            date = datetime.strptime(datum['date'], '%Y-%m-%d %H:%M:%S').date()
            if datum['value'] is None:
                energy = 0
            else:
                energy = int(datum['value'])
            energy_list.append({'date': date, 'energy': energy})
            try:
                date_entry = EnergyPerDay.objects.get(date=date)
                if date + timedelta(days=5) < date.today():
                    date_entry.energy = energy
            except EnergyPerDay.DoesNotExist:
                new_row = EnergyPerDay.objects.create(date=date, energy=energy)
                new_row.save()
        return JsonResponse({'energy': energy_list, 'success': True})
    print({'energy': [], 'success': False})

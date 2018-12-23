""" Sends all requests to right view """
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('password_reset', views.password_reset_view, name='password_reset'),

    path('chart/day', views.chart_day_view, name='chart_day'),
    path('chart/week', views.chart_week_view, name='chart_week'),
    path('chart/year', views.chart_year_view, name='chart_year'),

    path('settings/user', views.user_settings_view, name='user_settings'),
    path('settings/charts', views.chart_settings_view, name='chart_settings'),

    path('json/icon', views.json_icon, name='json_icon'),
    path('json/energy', views.json_energy_day_view, name='json_energy_day')
]

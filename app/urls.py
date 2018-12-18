""" Sends all requests to right view """
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('password_reset', views.password_reset_view, name='password_reset'),
    path('settings/user', views.user_settings_view, name='user_settings'),
    path('settings/charts', views.chart_settings_view, name='chart_settings'),
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('login_and_register', views.login_and_register, name='login_and_register'),
]

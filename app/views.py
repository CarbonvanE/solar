""" All view logic for the app """

from uuid import uuid4

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.models import CustomUser, SuperSecretCode


def index_view(request):
    """ Main page of the app """
    return render(request, 'app/index.html')


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
    return render(request, 'app/login.html')

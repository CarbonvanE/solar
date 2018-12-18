""" All view logic for the app """

from uuid import uuid4

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.models import CustomUser, SuperSecretCode

@login_required
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


@login_required
def logout_view(request):
    """ Log the user out """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def password_reset_view(request):
    """ TODO: Create the password reset logic """
    return render(request, 'app/login.html', {'message': 'Hahaha, too bad...'})


@login_required
def user_settings_view(request):
    """ Returns the settings page """
    if request.method == 'GET':
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        context = {
            'tab': 'settings',
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        }
        return render(request, 'app/user_settings.html', context)
    elif request.method == 'POST':
        user = CustomUser.objects.filter(email=request.user).first()
        code = request.POST['code']
        content = request.POST['content']
        if code == 'first_name':
            user.first_name = content
        elif code == 'last_name':
            user.last_name = content
        elif code == 'email':
            user.email = content
        elif code == 'password':
            user.set_password(content)
            login(request, user)
        user.save()
        return HttpResponseRedirect(reverse('user_settings'))

@login_required
def chart_settings_view(request):
    return render(request, 'app/chart_settings.html', {'tab': 'settings'})

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
            if form['password'] != form['password-check']:
                return render(request, 'app/login.html', {'message': 'Passwords do not match.'})
            if CustomUser.objects.filter(email=form['email']).exists():
                message = 'This e-mail address already has an account.'
                return render(request, 'app/login.html', {'message': message})
            if not SuperSecretCode.objects.filter(code=form['super-secret-code']).exists():
                message = 'This super secret code does not exist.'
                return render(request, 'app/login.html', {'message': message})
            code = SuperSecretCode.objects.filter(code=form['super-secret-code']).first()
            if code.activated:
                message = 'This super secret code has already been used.'
                return render(request, 'app/login.html', {'message': message})
            new_user = CustomUser.objects.create_user(email=form['email'],\
                first_name=form['first-name'],\
                password=form['password'],\
                username=uuid4())
            new_user.save()
            code.activated = True
            code.user = new_user
            code.save()
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

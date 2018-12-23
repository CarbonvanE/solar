""" Handles all the settings pages """

from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from app.models import CustomUser


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
        'tab': 'settings'
    }
    return render(request, 'app/chart_settings.html', context)

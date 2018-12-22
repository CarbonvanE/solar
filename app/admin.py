from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from .models import SuperSecretCode
from .models import EnergyPerDay


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'first_name',]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SuperSecretCode)
admin.site.register(EnergyPerDay)

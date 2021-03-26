from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms
from django.db import models

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields =('username', 'email')



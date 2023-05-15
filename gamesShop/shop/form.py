from django import forms
from .models import GameDetail
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class AddGameForm(forms.ModelForm):
    class Meta:
        model = GameDetail
        fields = ('cover', 'label', 'developer', 'publisher', 'release_date', 'price', 'description')


class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']

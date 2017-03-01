from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput) #teksten som tastes inn kommer som ***

    class Meta: #info om klassen
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password'] #feltene som brukerne skal fylle ut (i den rekkefolgen)

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']
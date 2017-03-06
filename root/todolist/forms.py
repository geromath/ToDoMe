from django.contrib.auth.models import User
from django import forms
from .models import Task

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

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_text', 'description']

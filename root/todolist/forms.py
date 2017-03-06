from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

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

class BootstrapModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class TaskForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)


    class Meta:
        model = Task
        widgets = {'due_date': forms.DateInput(attrs={'id': 'inputDate'})}
        fields = ['task_text', 'description', 'due_date']


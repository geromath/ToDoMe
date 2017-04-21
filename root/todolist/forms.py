from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, TextInput
from .models import Task, UserProfile


class UserForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:  # info om klassen
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']  # feltene som brukerne skal
        # fylle ut (i
        #  den rekkefolgen)


class LoginForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"


class BootstrapModelForm(ModelForm):
    task_text = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'Name your TODO'}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder':
                                                                                        'Describe your TODO',
                                                                                    'rows': 6}))
    due_date = forms.DateTimeField(label='Due Date', required=False, widget=forms.DateInput(attrs={'id':
                                                                                                       'inputDate',
                                                                                                   'placeholder':
                                                                                                       'Select Due '
                                                                                                       'Date ('
                                                                                                       'Optional)',
                                                                                                   'weekStart': 1}))
    color = forms.CharField(label="Color", widget=forms.TextInput(attrs={'type': 'color', 'value': '#808080'}))

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
        fields = ['task_text', 'description', 'due_date', 'color']

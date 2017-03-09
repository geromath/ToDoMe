from django.contrib.auth.models import User
from django import forms
from django.core.files.images import get_image_dimensions

from django.forms import ModelForm

from .models import Task, UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput) #teksten som tastes inn kommer som ***

    class Meta: # info om klassen
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password'] #feltene som brukerne skal fylle ut (i den rekkefolgen)


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        # avatar = models.ImageField(upload_to='/images/)
        try:
            w, h = get_image_dimensions(avatar)
            #validate dimensions
            max_width = max_height = 100
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                    'GIF or PNG image.')

            #validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(u'Avatar file size may not exceed 20k.')

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar

class BootstrapModelForm(ModelForm):
    task_text = forms.CharField(label="Title", widget=forms.TextInput)
    description = forms.CharField(label='Description', widget=forms.Textarea)


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



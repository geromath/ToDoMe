#denne maa inkluderes i root-url-filen
from django.conf.urls import url
from . import views

app_name = 'todolist'

urlpatterns = [

    url(r'^register/$', views.UserFormView.as_view(), name='register'),

]
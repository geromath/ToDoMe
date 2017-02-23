from django.conf.urls import url
from . import views

app_name = 'todolist'

urlpatterns = [

    # Main view
    url(r'^$', views.index, name="index"),

    # Registrering
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # Make new task
    url(r'^mktsk/$', views.TaskCreate.as_view(), name='make_task'),

    # Update task
    url(r'^mktsk/(?P<pk>[0-9]+)/$', views.TaskUpdate.as_view(), name='update_task'),

    # Delete task
    url(r'^mktsk/(?P<pk>[0-9]+)/delete/$', views.TaskDelete.as_view(), name='delete_task'),
]






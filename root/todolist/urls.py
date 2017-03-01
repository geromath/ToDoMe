from django.conf.urls import url
from django.contrib.auth import views as auth_views, login, authenticate
from . import views

app_name = 'todolist'

urlpatterns = [
    # All of the below are subpages of /todolist/

    # Index view (log in screen)
    url(r'^$', auth_views.login, kwargs={'template_name': 'todolist/login.html'}, name='login'),

    # Main view
    url(r'^todo/$', views.todo, name="todo"),

    # Registrering
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # Make new task
    url(r'^mktsk/$', views.TaskCreate.as_view(), name='make_task'),

    # Update task
    url(r'^mktsk/(?P<pk>[0-9]+)/$', views.TaskUpdate.as_view(), name='update_task'),

    # Delete task
    url(r'mktsk/(?P<pk>[0-9]+)/delete/$', views.TaskDelete.as_view(), name='delete_task'),
]






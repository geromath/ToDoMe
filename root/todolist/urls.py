from django.conf.urls import url
from django.contrib.auth import views as auth_views, login, authenticate
from . import views

app_name = 'todolist'

urlpatterns = [
    # All of the below are subpages of /todolist/
    # Index view (log in screen)
    url(r'^$', views.avatar_screen, name='avatar_screen'),

    # Login screen
    url(r'^login$', auth_views.login, kwargs={'template_name': 'accounts/login.html'}, name='login'),

    # Accounts
    url(r'^accounts/login$', auth_views.login, kwargs={'template_name': 'accounts/login.html'}, name='login'),

    # Main view
    url(r'^todo/$', views.todo, name="todo"),

    # Detail view
    url(r'^todo/(?P<id>\d+)/$', views.todo_detail, name="todo_detail"),

    # Archived (Completed) TODOs
    url(r'^archive/$', views.archive, name="archive"),

    # Registrering
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # Make new task
    url(r'^mktsk/$', views.TaskCreate.as_view(), name='make_task'),

    # Update task v2
    url(r'^todo/(?P<id>\d+)/edit/$', views.todo_update, name='update_task'),

    # Update task
    # url(r'^mktsk/(?P<id>\d+)/$', views.TaskUpdate.as_view(), name='update_task'),

    # Archive task
    url(r'archive/(?P<pk>[0-9]+)/archive', views.task_checked, name='task_checked'),

    # Delete task
    url(r'delete/(?P<pk>[0-9]+)/delete/$', views.TaskDelete.as_view(), name='delete_task'),

]






from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'todolist'

urlpatterns = [
    # All of the below are subpages of /todolist/

    # Login screen
    url(r'^login/$', auth_views.login, name='login', kwargs={'redirect_authenticated_user': True}),
    url(r'^logout/$', auth_views.logout, name='logout'),

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

    # Update task
    url(r'^todo/(?P<id>\d+)/edit/$', views.todo_update, name='update_task'),

    # Archive task
    url(r'archive/(?P<pk>[0-9]+)/archive/$', views.task_checked, name='task_checked'),

    # Delete task
    url(r'delete/(?P<pk>[0-9]+)/delete/$', views.TaskDelete.as_view(), name='delete_task'),

    # For Facebook login
    url(r'^oauth/', include('social_django.urls', namespace='social')),

    # My Profile
    url(r'^profile/$', views.profile, name="profile"),

]

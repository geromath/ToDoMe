from django.conf.urls import url

from .views import QuizListView, QuizTake

app_name = 'quizzes'

urlpatterns = [

    url(regex=r'^$',
        view=QuizListView.as_view(),
        name='quiz_index'),

    #  passes variable 'slug' to the quiz_take view
    url(regex=r'^(?P<slug>[\w-]+)/$',
        view=QuizTake.as_view(),
        name='quiz_take'),

]


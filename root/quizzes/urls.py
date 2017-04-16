from django.conf.urls import url

from . import views
from .views import QuizListView, CategoriesListView,\
    ViewQuizListByCategory, QuizUserProgressView, QuizMarkingList,\
    QuizMarkingDetail, QuizDetailView, QuizTake


app_name = 'quizzes'

urlpatterns = [
    #url(r'^$', views.index, name='index'),

#https://docs.djangoproject.com/en/1.10/topics/class-based-views/generic-display/
# All of the below are subpages of /quizzes/

    url(regex=r'^$',
        view=QuizListView.as_view(),
        name='quiz_index'),

    #  passes variable 'quiz_name' to quiz_take view
    url(regex=r'^(?P<slug>[\w-]+)/$',
        # r'^(?P<quiz_name>[\w-]+)/take/$' ELLER teste: r'^(?P<quiz_id>[0-9]+)/take/$' ELLER r'^(?P<slug>[\w-]+)/$'
        view=QuizTake.as_view(),
        name='quiz_take'),


    url(regex=r'^(?P<slug>[\w-]+)/$',  #OBS! se paa '-'i denne r'^(?P<slug>[\w-]+)/$' ELLER teste: r'^(?P<pk>[\d.]+)/$'
        view=QuizDetailView.as_view(),
        name='quiz_start_page'),

    #  passes variable 'pk' to quiz_take view. BRUKES IKKE
    url(regex=r'^(?P<pk>[\d.]+)/$',  #tester denne. Skal kontrollere om rett svar.
        view=QuizTake.as_view(),
        name='checkanswer'),







    url(regex=r'^category/$',
        view=CategoriesListView.as_view(),
        name='quiz_category_list_all'),

    url(regex=r'^category/(?P<category_name>[\w|\W-]+)/$',
        view=ViewQuizListByCategory.as_view(),
        name='quiz_category_list_matching'),

    url(regex=r'^progress/$',
        view=QuizUserProgressView.as_view(),
        name='quiz_progress'),

    url(regex=r'^marking/$',
        view=QuizMarkingList.as_view(),
        name='quiz_marking'),

    url(regex=r'^marking/(?P<pk>[\d.]+)/$',
        view=QuizMarkingDetail.as_view(),
        name='quiz_marking_detail'),



]


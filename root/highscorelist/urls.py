__author__ = 'caroline1'
from root.highscorelist.views import ScoresView
from django.conf.urls.defaults import *

app_name = 'highscorelist'

urlpatterns = [
    # Main view
    url(r'^highscores', ScoresView.as_view, name="leaderboard_highscores"),

    # Update leaderboard
    url(r'^leaderboard', ScoresView.leaderboard.as_view(), name='update_leaderboard'),

]



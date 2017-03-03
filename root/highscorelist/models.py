from django.db import models
from django.urls import reverse


class leaderboard(models.Model):
    scores = models.IntegerField()
    user = models.CharField(max_length=150)

    def get_absolute_url(self):
        return reverse('highscorelist:index')

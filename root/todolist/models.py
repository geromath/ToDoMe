from django.db import models
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import User


class Task(models.Model):
    task_text = models.CharField(max_length = 150)
    description = models.CharField(max_length = 400)
    # due_date = models.DateField()
    # archived = models.BooleanField()

    def get_absolute_url(self):
        return reverse('todolist:index')

    def __str__(self):
        return self.task_text


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField()

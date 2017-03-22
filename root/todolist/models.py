from django.db import models
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import User
from oauth2client.contrib.django_orm import FlowField
from oauth2client.contrib.django_orm import CredentialsField
from oauth2client.contrib.django_orm import Storage

class Task(models.Model):
    task_text = models.CharField(max_length = 150)
    description = models.TextField(max_length = 500)
    due_date = models.DateField(default=None, null=True, blank=True)
    archived = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def get_absolute_url(self):
        return reverse('todolist:index', kwargs={"id": self.id})

    def __str__(self):
        return self.task_text

    class Meta:
        ordering = ["-time_created"]


class FlowModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    flow = FlowField()

class CredentialsModel(models.Model):
    id = models.ForeignKey(User, primary_key=True)
    credential = CredentialsField()


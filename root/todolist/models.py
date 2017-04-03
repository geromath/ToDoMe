from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import admin

class TaskManager(models.Manager):

    def active(self, *args, **kwargs):
        return super(TaskManager, self).filter(archived=False)
    def archived(self, *args, **kwargs):
        return super(TaskManager, self).filter(archived=True)

class Task(models.Model):
    task_text = models.CharField(max_length = 150)
    description = models.TextField(max_length = 500)
    due_date = models.DateField(default=None, null=True, blank=True)
    archived = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    user = models.ForeignKey(User, null=True, blank=True)

    objects = TaskManager()

    def get_absolute_url(self):
        return reverse('todolist:index', kwargs={"id": self.id})

    def __str__(self):
        return self.task_text

    class Meta:
        ordering = ["-time_created"]

class TaskAdmin(admin.ModelAdmin):
    fields = ['task_text', 'description', 'due_date']
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super.save_model(request, obj, form, change)

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def __str__(self):
        return self.user

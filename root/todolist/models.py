from django.db import models
from django.core.urlresolvers import reverse, reverse_lazy

class Task(models.Model):
    task_text = models.CharField(max_length = 150)
    description = models.TextField(max_length = 500)
    due_date = models.DateField(default=None, null=True, blank=True)
    archived = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('todolist:index')

    def __str__(self):
        return self.task_text

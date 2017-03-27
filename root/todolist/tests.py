import datetime

from django.contrib.admin import AdminSite
from django.contrib.admin import ModelAdmin
from django.test import TestCase
from django.urls import resolve
from django.urls import reverse

from .models import Task


# Create your tests here.



class TaskTestCase(TestCase):
    def setUp(self):
        Task.objects.create(task_text="Homework", description="Do my homework", due_date=None, archived=False)
        current_date = datetime.date(2017, 3, 27)
        Task.objects.create(task_text="Take a quiz", description="Complete quiz regarding TDT4145",
                            due_date=current_date)
        Task.objects.create(task_text=13, description="")

    def testTaskInfo(self):
        homework = Task.objects.get(task_text="Homework")
        quiz = Task.objects.get(description="Complete quiz regarding TDT4145")
        today = datetime.date(2017, 3, 27)

        self.assertEqual("Homework", homework.task_text)
        self.assertIs(homework.archived, False)
        self.assertEqual(today, quiz.due_date)

    def test_todo(self):
        resp = self.client.get('/todo/')
        self.assertEqual(resp.status_code, 302)

        # Ensure that non-existent todos throw a 404.
        resp = self.client.get('/todo_detail/485438528345/')
        self.assertEqual(resp.status_code, 404)


class UrlTestCase(TestCase):
    def testReverseResolve(self):

        register_resolver = resolve('/register/')
        self.assertEqual(register_resolver.view_name, 'todolist:register')

        login_resolver = resolve('/login/')
        self.assertEqual(login_resolver.view_name, 'todolist:login')

        logout_resolver = resolve('/logout/')
        self.assertEqual(logout_resolver.view_name, 'todolist:logout')


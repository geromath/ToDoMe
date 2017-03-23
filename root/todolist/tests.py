from django.test import TestCase
from django.urls import resolve
from django.urls import reverse

from root.todolist.models import Task

# Create your tests here.

class TaskTestCase(TestCase):
    def setUp(self):
        Task.objects.create(task_text="Homework", description="Do my homework", due_date="", archived=False)
        Task.objects.create(task_text="Take a quiz", description="Complete quiz regarding TDT4145",
                            due_date="03/22/2017")
        Task.objects.create(task_text=13, description="")

    def testTaskInfo(self):
        homework = Task.objects.get(task_text="Homework")
        quiz = Task.objects.get(description="Complete quiz regarding TDT4145")

        self.assertEqual("Homework", homework.task_text)
        self.assertIs(homework.archived, False)
        self.assertEqual("03/22/2017", quiz.due_date)

class UrlTestCase(TestCase):
    def testReverseResolve(self):
        url = reverse('todo_detail', args=[53])
        self.assertEqual(url, '/archive/53')

        register_resolver = resolve('/register/')
        self.assertEqual(register_resolver.view_name, 'register')

        login_resolver = resolve('/login/')
        self.assertEqual(login_resolver.view_name, 'login')

        logout_resolver = resolve('/logout/')
        self.assertEqual(logout_resolver.view_name, 'logout')
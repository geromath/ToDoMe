from django.test import TestCase
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
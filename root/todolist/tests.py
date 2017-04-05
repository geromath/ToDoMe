import datetime
from django.test import Client
from django.test import TestCase
from django.urls import resolve
from .models import Task


class TaskTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('Pekka123')
        user.save()

        Task.objects.create(task_text="Homework", description="Do my homework", due_date=None, archived=False)
        current_date = datetime.date(2017, 3, 27)
        Task.objects.create(task_text="Take a quiz", description="Complete quiz regarding TDT4145",
                            due_date=current_date)
        Task.objects.create(task_text=13, description="")

        self.task_1 = Task.objects.get(pk=1)
        self.task_2 = Task.objects.get(pk=2)

    def test_task_creation(self):
        c = Client()  # instantiate the Django test client
        logged_in = c.login(username='testuser', password='Pekka123')
        response = c.post('/todo/', {'task_text': 'Some title', 'description': 'Some text'}, follow=True)

        self.assertEqual(response.redirect_chain, [('/todo/', 302)])
        self.assertContains(response, 'Some title')
        self.assertContains(response, 'Some text')

    def testTaskInfo(self):
        homework = Task.objects.get(task_text="Homework")
        quiz = Task.objects.get(description="Complete quiz regarding TDT4145")
        today = datetime.date(2017, 3, 27)

        self.assertEqual("Homework", homework.task_text)
        self.assertIs(homework.archived, False)
        self.assertEqual(today, quiz.due_date)
        self.assertIn(homework.task_text, "Homework")

    def test_todo(self):
        resp = self.client.get('/todo/')
        self.assertEqual(resp.status_code, 302)

        # Ensure that non-existent todos throw a 404.
        resp = self.client.get('/todo_detail/485438528345/')
        self.assertEqual(resp.status_code, 404)


    def create_task(self, title="only a test", body="yes, this is only a test"):
        return Task.objects.create(task_text=title, description=body)

    def test_whatever_creation(self):
        t = self.create_task(body="Jau")
        self.assertTrue(isinstance(t, Task))
        self.assertEqual(t.__str__(), t.task_text)
        self.assertEqual(str(t), t.task_text)


class UrlTestCase(TestCase):
    def testReverseResolve(self):
        register_resolver = resolve('/register/')
        self.assertEqual(register_resolver.view_name, 'todolist:register')

        login_resolver = resolve('/login/')
        self.assertEqual(login_resolver.view_name, 'todolist:login')

        logout_resolver = resolve('/logout/')
        self.assertEqual(logout_resolver.view_name, 'todolist:logout')

class TestUserInformation(TestCase):

    def testUser(self):
        user = User.objects.create(username='testuser')
        self.assertEqual(str(user), user.username)

class TestCalls(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('Pekka123')
        user.save()

    def test_login_required(self):
        response = self.client.get('/todo/', follow=True)
        self.assertRedirects(response, '/login/?next=/todo/')
        response = self.client.post('/archive/', follow=True)
        self.assertRedirects(response, '/login/?next=/archive/')

    def test_call_view_loads(self):
        self.client.login(username='testuser', password='Pekka123')
        response = self.client.get('/todo/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todolist/index.html')

    def test_call_view_fails_blank(self):
        self.client.login(username='testuser', password='Pekka123')
        response = self.client.post('/todo/', {})  # blank data dictionary
        self.assertFormError(response, 'form', 'task_text', 'This field is required.')
        # etc. ...

    def test_call_view_fails_invalid(self):
        self.client.login(username='testuser', password='Pekka123')
        response = self.client.post('/todo/', {'task_text': 'Some title THAT IS FAR TOOO '
                                                            'LONGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG',
                                               'description': 'Some '
                                                              'text'})  # invalid data dictionary
        self.assertFormError(response, 'form', 'task_text',
                             'Ensure this value has at most 150 characters (it has 283).')

    def test_call_view_fails_valid(self):
        self.client.login(username='testuser', password='Pekka123')
        response = self.client.post('/todo/',
                                    {'task_text': 'Some title', 'description': 'Some text'})  # valid data dictionary
        self.assertRedirects(response, '/todo/')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import View, CreateView, UpdateView, DeleteView
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from .models import Task
from .forms import TaskForm
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from quizzes.models import Progress
from quizzes.models import Quiz
from quizzes.models import Sitting

import datetime



@login_required(login_url='todolist:login')
def archive(request):
    all_tasks = Task.objects.filter(user=request.user)
    task_count = Task.objects.filter(archived=True).filter(user=request.user).count()

    # Search function for archived TODOs
    queryset_list = Task.objects.archived()
    query = request.GET.get("q")
    if query:
        all_tasks = queryset_list.filter(
            Q(task_text__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

    context = {
        'nbar': 'archive',
        'all_tasks': all_tasks,
        'task_count': task_count,
        'title': 'Archive',
    }
    return render(request, 'todolist/archive.html', context)

@login_required(login_url='todolist:login')
def avatar_screen(request):
    today = datetime.date.today()
    overdue_tasks = Task.objects.filter(user=request.user).filter(due_date__lte=today).filter(archived=False)
    close_tasks_all = Task.objects.filter(user=request.user).exclude(due_date__lte=today).order_by('due_date')

    close_tasks = []
    i = 0
    for task in close_tasks_all:
        if (i < 3 and not task.archived):
            close_tasks.append(task)
            i += 1

    sittings = Sitting.objects.filter(user=request.user)
    quizzes_done = []
    for sit in sittings:
        quizzes_done.append(sit.quiz.title)

    quizzes = Quiz.objects.all()
    quiz_notify = []
    for element in quizzes:
        if element.title not in quizzes_done:
            quiz_notify.append(element)


#    print("You have taken" ,len(quizzes_done), "quiz, and it is ... ", quizzes_done) if we want to show quizzes done

    context = {
        'overdue_tasks': overdue_tasks,
        'close_tasks': close_tasks,
        'quiz_notify': quiz_notify,
        'title': 'ToDoMe',
    }
    return render(request, 'todolist/avatar_screen.html', context)


@login_required(login_url='todolist:login')
def todo(request):
    all_tasks = Task.objects.filter(user=request.user)
    task_count = Task.objects.filter(archived=False).filter(user=request.user).count()

    # Search function for active TODOs
    queryset_list = Task.objects.active()
    query = request.GET.get("q")
    if query:
        all_tasks = queryset_list.filter(
            Q(task_text__icontains=query) |
            Q(description__icontains=query)
        ).distinct()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect(reverse('todolist:todo'))
        else:
            messages.error(request, message="error")
    else:
        form = TaskForm()

    context = {
        'all_tasks': all_tasks,
        'task_count': task_count,
        'form': form,
        'nbar': 'home',
        'title': 'TODOs',
        'queryset_list': queryset_list
    }

    return render(request, 'todolist/index.html', context)


@login_required(login_url='todolist:login')
def todo_detail(request, id=None):
    instance = get_object_or_404(Task, id=id)
    context = {
        "title": 'Detail',
        "instance": instance,
    }
    return render(request, "todolist/todo_detail.html", context)


# Made a separate method for updating todos, seems to work, just need to implement it with modals somehow..
@login_required(login_url='todolist:login')
def todo_update(request, id=None):
    instance = get_object_or_404(Task, id=id)
    form = TaskForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(reverse("todolist:todo"))

    context = {
        "task_text": instance.task_text,
        "task_description": instance.description,
        "due_date": instance.due_date,
        "instance": instance,
        "form": form,
    }
    return render(request, "todolist/edit_task.html", context)


@login_required(login_url='todolist:login')
def profile(request):
    user = request.user

    context = {
        'nbar': 'profile',
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'username': user.username,
        'title': 'Profile',
    }
    return render(request, 'todolist/profile.html', context)


class TaskCreate(CreateView):
    model = Task
    fields = ['task_text', 'description']


class TaskUpdate(UpdateView):
    model = Task
    fields = ['task_text', 'description']


class TaskDelete(DeleteView):
    model = Task

    def get_success_url(self):
        referer_url = self.request.META.get('HTTP_REFERER')  # get the referer url from request's 'META' dictionary
        if referer_url:
            return referer_url  # return referer url for redirection

    def form_valid(self, form):
        self.object = form.save()

        # Does not redirect if valid
        # return HttpResponseRedirect(self.get_success_url())

        # Render the template
        # get_context_data populates object in the context
        # or you also get it with the name you want if you define context_object_name in the class
        return self.render_to_response(self.get_context_data(form=form))


def task_checked(request, pk):
    task = Task.objects.get(pk=pk)
    referer = request.META.get('HTTP_REFERER')
    if ("/archive/" in referer):
        task.archived = False
        task.save()
        return HttpResponseRedirect(reverse("todolist:archive"))
    else:
        task.archived = True
        task.save()
        return HttpResponseRedirect(referer)


class UserFormView(View):
    form_class = UserForm  # blueprint til det vi skal bruke

    template_name = 'todolist/registration_form.html'

    # display blank form
    def get(self, request):  # innebygd funksjon for get-requests. f.eks. laste inn skjema som skal fylles ut
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # legge til brukeren i databasen
    def post(self, request):  # innebygd funksjon for post-requests
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # cleaned normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            user.set_password(password)
            user.save()  # lagrer brukeren i databasen

            # Returns User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:  # dersom de ikke er banned/utestengt etc

                    login(request, user)

                    return redirect(
                        'todolist:avatar_screen')  # maa ogsaa lages! Sender brukeren til startsiden etter registrering?(login)

        return render(request, self.template_name, {'form': form})  # gir skjemaet paa nytt om noe gikk galt

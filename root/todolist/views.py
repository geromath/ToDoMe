from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import View, CreateView, UpdateView, DeleteView
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

#importerer forms-klassen vi lagde
from .models import Task
from .forms import TaskForm
from django.core.urlresolvers import reverse_lazy, reverse

from django.http import HttpResponse

def index(request):

    context = {
        'nbar': 'startpage'
    }
    return render(request, 'todolist/startpage.html', context)


def archive(request):
    all_tasks = Task.objects.all()
    task_count = Task.objects.filter(archived=True).count()
    context = {
        'nbar': 'archive',
        'all_tasks': all_tasks,
        'task_count': task_count,
        'title': 'Archive',
    }
    return render(request, 'todolist/archive.html', context)

@login_required
def todo(request):
    all_tasks = Task.objects.all()
    task_count = Task.objects.filter(archived=False).count()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('todolist:todo'))
        else:
            messages.error()
    else:
        form = TaskForm()

    context = {
        'all_tasks': all_tasks,
        'task_count': task_count,
        'form': form,
        'nbar': 'home',
        'title': 'TODOs',
    }

    return render(request, 'todolist/index.html', context)

def todo_detail(request, id=None):
    instance = get_object_or_404(Task, id=id)
    context = {
        "title": 'Detail',
        "instance": instance,
    }
    return render(request, "todolist/todo_detail.html", context)

# Made a separate method for updating todos, seems to work, just need to implement it with modals somehow..
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

class TaskCreate(CreateView):
    model = Task
    fields = ['task_text', 'description']

class TaskUpdate(UpdateView):
    model = Task
    fields = ['task_text', 'description']

class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('todolist:todo')

def task_checked(request, pk):
    task = Task.objects.get(pk=pk)
    task.archived = True
    task.save()
    return render(request, "todolist/index.html", None)


class UserFormView(View):
    form_class = UserForm #blueprint til det vi skal bruke

    template_name = 'todolist/registration_form.html' #maa lages!

    #display blank form
    def get(self, request): #innebygd funksjon for get-requests. f.eks. laste inn skjema som skal fylles ut
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    #legge til brukeren i databasen
    def post(self, request): #innebygd funksjon for post-requests
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            #cleaned normalized data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            user.set_password(password)
            user.save() #lagrer brukeren i databasen

            #Returns User object if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active: #dersom de ikke er banned/utestengt etc

                    login(request, user)

                    return redirect('todolist:todo') #maa ogsaa lages! Sender brukeren til startsiden etter registrering?(login)

        return render(request, self.template_name, {'form': form}) #gir skjemaet paa nytt om noe gikk galt









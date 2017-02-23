from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View, CreateView, UpdateView, DeleteView
from .forms import UserForm
#importerer forms-klassen vi lagde
from .models import Task
from django.core.urlresolvers import reverse_lazy

from django.http import HttpResponse

def index(request):
    all_tasks = Task.objects.all()
    context = {
        'all_tasks': all_tasks
    }
    return render(request, 'todolist/index.html', context)

class TaskCreate(CreateView):
    model = Task
    fields = ['task_text', 'description']

class TaskUpdate(UpdateView):
    model = Task
    fields = ['task_text', 'description']

class TaskDelete(DeleteView):
    model = Task
    success_url = reverse_lazy('todolist:index')

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

                    return redirect('todolist:index') #maa ogsaa lages! Sender brukeren til startsiden etter login

        return render(request, self.template_name, {'form': form}) #gir skjemaet paa nytt om noe gikk galt









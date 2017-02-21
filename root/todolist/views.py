from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    all_tasks = Task.objects.all()
    context = {
        'all_tasks': all_tasks
    }
    return render(request, 'todolist/index.html', context)




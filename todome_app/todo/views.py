from django.http import Http404
from django.shortcuts import render
from .models import Todo
from django.template import loader

def index(request):
    todo_list = Todo.objects.order_by('-date')
    context = {
        'todo_list': todo_list,
    }
    return render(request, 'index.html', context)
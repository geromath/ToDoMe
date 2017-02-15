from django.http import HttpResponse
from .models import Todo
from django.template import loader

def index(request):
    todo_list = Todo.objects.order_by('-date')
    template = loader.get_template('index.html')
    context = {
        'todo_list': todo_list,
    }
    return HttpResponse(template.render(context, request))
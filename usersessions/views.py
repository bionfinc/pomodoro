from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q

from usersessions.models import Task

# Create your views here.
def tasks_view(request):
    user = User.objects.get(username=request.user.username)

    searchquery = request.GET.get('search')

    if searchquery != None:
        tasks = Task.objects.filter(Q(task_name__icontains=searchquery) 
                                  | Q(subcategory__icontains=searchquery))
    else:
        tasks = Task.objects.all()

    context = {
        'user': user,
        'tasks': tasks
    }

    return render(request, 'usersessions/tasks.html', context)
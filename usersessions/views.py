from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.core.paginator import Paginator

from usersessions.models import Task, UserSession


# Create your views here.
def tasks_view(request):
    user = User.objects.get(username=request.user.username)

    searchquery = request.GET.get('search')
    page_num = request.GET.get('page')

    if searchquery != None:
        tasks = Task.objects.filter(Q(task_name__icontains=searchquery) 
                                  | Q(category__icontains=searchquery))
    else:
        tasks = Task.objects.all()

    for task in tasks:
        # Determine the first start date for the task
        task.first_time_start = Task.objects.filter(task_name__icontains=task.task_name).latest('time_start').time_start

    # Set up the page system for displaying data
    paginator = Paginator(tasks, 5) # Show 5 tasks per page.
    tasks_page = paginator.get_page(page_num)

    context = {
        'user': user,
        'tasks': tasks_page
    }

    return render(request, 'usersessions/tasks.html', context)




def sessions_view(request):
    user = User.objects.get(username=request.user.username)

    searchquery = request.GET.get('search')
    page_num = request.GET.get('page')

    if searchquery != None:
        sessions = UserSession.objects.filter(session_name__icontains=searchquery)

    else:
        sessions = UserSession.objects.all()


    for session in sessions:
        # Determine the first start date for the session
        session.first_time_start = UserSession.objects.filter(session_name__icontains=session.session_name).latest('session_time_start').session_time_start

    # Set up the page system for displaying data
    paginator = Paginator(sessions, 5) # Show 5 sessions per page.
    tasks_page = paginator.get_page(page_num)

    context = {
        'user': user,
        'sessions': tasks_page
    }

    return render(request, 'usersessions/sessions.html', context)
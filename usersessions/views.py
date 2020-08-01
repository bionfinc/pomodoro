from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum
from django.core.paginator import Paginator

from usersessions.models import Task, UserSession


# Create your views here.
def tasks_view(request):
    user = User.objects.get(username=request.user.username)

    searchquery = request.GET.get('search')
    page_num = request.GET.get('page')

    #TODO Make not delete multiple categories
    if request.POST.__contains__('delete'):
        Task.objects.filter(
                                task_name__exact=request.POST.get('delete'),
                                usersession__user__username__exact=user
                            ).delete()

    if searchquery != None:
        tasks = Task.objects.filter(
                                Q(task_name__icontains=searchquery) 
                                | Q(category__icontains=searchquery),
                                usersession__user__username__exact=user
                                )
    else:
        tasks = Task.objects.filter(usersession__user__username__exact=user)

    tasks = tasks.values(
                    'task_name', 
                    'category'
                ).annotate(
                    sessions_count=Count('pk', distinct=True), 
                    total_task_time=Sum('task_time')
                )

    for task in tasks:
        # Determine the first start date for the task
        task['first_time_start'] = Task.objects.filter(task_name__exact=task.get('task_name')).earliest('time_start').time_start

    # Set up the page system for displaying data
    paginator = Paginator(tasks, 10) # Show 10 tasks per page.
    tasks_page = paginator.get_page(page_num)

    context = {
        'user': user,
        'tasks_page': tasks_page
    }

    return render(request, 'usersessions/tasks.html', context)


def task_detail_view(request):
    user = User.objects.get(username=request.user.username)
    task_name = request.GET.get('action')

    #TODO add user validation

    #TODO does not get the right individual task, probably better to get a collective

    task = Task.objects.filter(task_name__icontains=task_name).earliest('time_start')
  
    context = {
        'user': user,
        'task': task
    }

    return render(request, 'usersessions/task_detail.html', context)


def sessions_view(request):
    user = User.objects.get(username=request.user.username)

    searchquery = request.GET.get('search')
    page_num = request.GET.get('page')

    #TODO add user validation
    if request.POST.__contains__('delete'):
        UserSession.objects.get(pk=request.POST.get('delete')).delete()

    if searchquery != None:
        sessions = UserSession.objects.filter(
                                            session_name__icontains=searchquery,
                                            user__username__exact=user
                                        )

    else:
        sessions = UserSession.objects.filter(user__username__exact=user)

    #determine the number of tasks done in session
    sessions = sessions.annotate(Count('task'))

    # Set up the page system for displaying data
    paginator = Paginator(sessions, 10) # Show 10 sessions per page.
    sessions_page = paginator.get_page(page_num)

    context = {
        'user': user,
        'sessions_page': sessions_page
    }

    return render(request, 'usersessions/sessions.html', context)


def session_detail_view(request):
    user = User.objects.get(username=request.user.username)
    session_num = request.GET.get('action')

    #TODO add user validation

    session = UserSession.objects.get(pk=session_num)

    tasks = Task.objects.filter(usersession__pk=session_num)
  
    context = {
        'user': user,
        'session': session,
        'tasks': tasks
    }

    return render(request, 'usersessions/session_detail.html', context)
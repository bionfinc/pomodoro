import datetime

from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q, Count, Sum
from django.core.paginator import Paginator

from usersessions.models import Task, UserSession


# View for the general task table page
def tasks_view(request):
    user = User.objects.get(username=request.user.username)

    # Get the GET request information
    searchquery = request.GET.get('search')
    page_num = request.GET.get('page')

    # If a delete request then remove all tasks that have that exact name and category.
    # Will only delete if also of the logged in user to protect against rigged POST requests
    if request.POST.__contains__('delete_name'):
        Task.objects.filter(
                                task_name__exact=request.POST.get('delete_name'),
                                category__exact=request.POST.get('delete_cat'),
                                usersession__user__username__exact=user,
                            ).delete()

    # Display all of the user's tasks, but groups by name and category. If the user specified a
    # specific name or category it will be filtered to that.
    if searchquery != None:
        tasks = Task.objects.filter(
                                    Q(task_name__icontains=searchquery) 
                                    | Q(category__icontains=searchquery),
                                    usersession__user__username__exact=user
                                )
    else:
        tasks = Task.objects.filter(usersession__user__username__exact=user)

    # Determines cumulative values for the task groups
    tasks = tasks.values(
                    'task_name', 
                    'category'
                ).annotate(
                    sessions_count=Count('pk', distinct=True), 
                    total_task_time=Sum('task_time')
                )

    # Populate the task groups with additional information not acquirable from the SQL calls
    for task in tasks:

        # Determine the first start date for the task group
        task['first_time_start'] = Task.objects.filter(
                                                    task_name__exact=task.get('task_name'),
                                                    category__exact=task.get('category'),
                                                    usersession__user__username__exact=user
                                                ).earliest('time_start').time_start

        # Format the total task time display
        task['total_task_time_hr'] = int(task['total_task_time'] / 60)
        task['total_task_time_min'] = task['total_task_time'] % 60

    # Set up the page system for displaying data
    paginator = Paginator(tasks, 10) # Show 10 tasks per page.
    tasks_page = paginator.get_page(page_num)

    context = {
        'user': user,
        'page_content': tasks_page
    }

    return render(request, 'usersessions/tasks.html', context)


# View for the task detail page
def task_detail_view(request):
    user = User.objects.get(username=request.user.username)
    
    # Get the GET request information
    task_name = request.GET.get('detail_name')
    task_category = request.GET.get('detail_cat')

    # Gets all the tasks associated with this selection and account
    subtasks = Task.objects.filter(
                                    task_name__exact=task_name,
                                    category__exact=task_category,
                                    usersession__user__username__exact=user
                                )

    # Get the first instance of this task group
    gen_task = subtasks.earliest('time_start')

    context = {
        'user': user,
        'gen_task': gen_task,
        'subtasks' : subtasks
    }

    return render(request, 'usersessions/task_detail.html', context)


# View for the general session table page
def sessions_view(request):
    user = User.objects.get(username=request.user.username)

    # Get the GET request information
    searchquery = request.GET.get('search')
    page_num = request.GET.get('page')

    # If a delete request then remove the selected session from the database
    if request.POST.__contains__('delete'):
        UserSession.objects.filter(
                                    user__username__exact=user
                                ).get(
                                    pk=request.POST.get('delete')
                                ).delete()

    # Display all of the user's sessions. If the user specified a
    # specific sessions name it will be filtered to that.
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
        'page_content': sessions_page
    }

    return render(request, 'usersessions/sessions.html', context)


# View for the session detail page
def session_detail_view(request):
    user = User.objects.get(username=request.user.username)

    # Get the GET request information
    session_num = request.GET.get('action')

    # Get the specified session if it is accociated with this user
    session = UserSession.objects.filter(
                                    user__username__exact=user
                                ).get(
                                    pk=session_num
                                )

    # Get the tasks of the session if it is accociated with this user
    tasks = Task.objects.filter(
                                    usersession__user__username__exact=user,
                                    usersession__pk=session_num
                                )
  
    context = {
        'user': user,
        'session': session,
        'tasks': tasks
    }

    return render(request, 'usersessions/session_detail.html', context)
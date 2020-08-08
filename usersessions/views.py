from django import forms
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from usersessions.models import Task, UserSession, TaskCategory
from .utils import get_info


class CreatNewCategory(forms.Form):
    newCategory = forms.CharField(label="New Category Name", max_length=100)


def tasks_view(request):
    user, search_query, page_num = get_info(request)

    # Will only delete if also of the logged in user to protect against rigged POST requests
    if request.POST.__contains__('delete_name'):
        Task.objects.filter(
            task_name__exact=request.POST.get('delete_name'),
            category__exact=request.POST.get('delete_cat'),
            usersession__user__username__exact=user,
        ).delete()

    # Display all of the user's tasks, but groups by name and category. If the user specified a
    # specific name or category it will be filtered to that.
    if search_query is not None:
        tasks = Task.objects.filter(
            Q(task_name__icontains=search_query)
            | Q(category__icontains=search_query),
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

    # Populate the task groups with additional information not acquirable from the SQL calls
    for task in tasks:
        task['first_time_start'] = Task.objects.filter(
            task_name__exact=task.get('task_name'),
            category__exact=task.get('category'),
            usersession__user__username__exact=user
        ).earliest('time_start').time_start

        task['total_task_time_hr'] = int(task['total_task_time'] / 60)
        task['total_task_time_min'] = task['total_task_time'] % 60

    paginator = Paginator(tasks, 10)
    tasks_page = paginator.get_page(page_num)

    context = {
        'user': user,
        'page_content': tasks_page
    }

    return render(request, 'usersessions/tasks.html', context)


def task_detail_view(request):
    user = User.objects.get(username=request.user.username)

    task_name = request.GET.get('detail_name')
    task_category = request.GET.get('detail_cat')

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
        'subtasks': subtasks
    }

    return render(request, 'usersessions/task_detail.html', context)


def sessions_view(request):
    user, search_query, page_num = get_info(request)

    if request.POST.__contains__('delete'):
        UserSession.objects.filter(
            user__username__exact=user
        ).get(
            pk=request.POST.get('delete')
        ).delete()

    if search_query is not None:
        sessions = UserSession.objects.filter(
            session_name__icontains=search_query,
            user__username__exact=user
        )

    else:
        sessions = UserSession.objects.filter(user__username__exact=user)

    sessions = sessions.annotate(Count('task'))

    paginator = Paginator(sessions, 10)
    sessions_page = paginator.get_page(page_num)

    context = {
        'user': user,
        'page_content': sessions_page
    }

    return render(request, 'usersessions/sessions.html', context)


def session_detail_view(request):
    user = User.objects.get(username=request.user.username)

    session_num = request.GET.get('action')

    session = UserSession.objects.filter(
        user__username__exact=user
    ).get(
        pk=session_num
    )

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


def categories_view(request):
    user, search_query, page_num = get_info(request)

    if request.POST.__contains__('delete'):
        TaskCategory.objects.filter(
            user__username__exact=user
        ).get(
            pk=request.POST.get('delete')
        ).delete()

    if search_query is not None:
        sessions = TaskCategory.objects.filter(
            task_category_name__icontains=search_query,
            user__username__exact=user
        )
    else:
        sessions = TaskCategory.objects.filter(user__username__exact=user)

    paginator = Paginator(sessions, 10)

    sessions_page = paginator.get_page(page_num)
    context = {
        'user': user,
        'page_content': sessions_page
    }

    return render(request, 'usersessions/categories.html', context)


def create_category_view(request):
    if request.method == "POST":
        form = CreatNewCategory(request.POST)
        if form.is_valid():
            new_category = form.cleaned_data['newCategory']
            current_user_id = request.user.id
            new_task_category = TaskCategory(user_id=current_user_id,
                                             task_category_name=new_category)
            new_task_category.save()
            return HttpResponseRedirect(
                reverse(
                    'categories'))  # returns the user to the timer, is not hard coded, uses the index name and reverses
        else:
            return HttpResponseRedirect(
                reverse('categories'))
            # if it wasnt a post render them the page
    return HttpResponseRedirect(
        reverse('categories'))

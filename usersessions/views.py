from django import forms
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from usersessions.models import Task, UserSession, TaskCategory
from .utils import get_info, get_task_information


class CreatNewCategory(forms.Form):
    newCategory = forms.CharField(label="New Category Name", max_length=100)


def tasks_view(request):
    user, tasks_page = get_task_information(request)

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

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum

from usersessions.models import Task


def get_info(request):
    user = User.objects.get(username=request.user.username)
    search_query = request.GET.get('search')
    page_num = request.GET.get('page')
    return user, search_query, page_num


def get_task_information(request):
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

    return user, tasks_page

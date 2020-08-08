from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# User session of pomodoro's intended to capture a period of activity
class UserSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    session_time_start = models.DateTimeField()
    session_time_end = models.DateTimeField(null=True)
    description = models.TextField(null=True)
    session_name = models.CharField(max_length=100)


# Single pomodoro task performed
class Task(models.Model):
    usersession = models.ForeignKey(
        UserSession,
        on_delete=models.CASCADE,
        null=True
    )
    task_time = models.IntegerField()
    task_name = models.CharField(max_length=100)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField(null=True)
    category = models.CharField(max_length=100, null=True)


# Task Category Names for a user of pomodoro's intended to capture a period of activity
class TaskCategory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    task_category_name = models.TextField(max_length=100, null=True)

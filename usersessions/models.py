from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# TODO Model description
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


# TODO Model description
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
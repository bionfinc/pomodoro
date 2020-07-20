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
	category = models.CharField(max_length=100, null=True) # TODO This might need a seperate table 
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
	task_description = models.TextField(null=True)
	subcategory = models.CharField(max_length=100, null=True)


# TODO Model description
class Rest(models.Model):
	usersession = models.ForeignKey(
		UserSession, 
		on_delete=models.CASCADE,
		null=True
	)
	rest_name = models.CharField(max_length=100)
	time_start = models.DateTimeField()
	time_end = models.DateTimeField()


# TODO Model description
class ShortRest(Rest):
    short_rest_time = models.IntegerField()


# TODO Model description
class LongRest(Rest):
    long_rest_time = models.IntegerField()
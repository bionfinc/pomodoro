from django.contrib import admin
from .models import UserSession, Task

# Register your models here.
admin.site.register(UserSession)
admin.site.register(Task)
from django.contrib import admin
from .models import UserSession, Task, ShortRest, LongRest

# Register your models here.
admin.site.register(UserSession)
admin.site.register(Task)
admin.site.register(ShortRest)
admin.site.register(LongRest)
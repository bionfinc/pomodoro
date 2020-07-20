"""pomodoro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from accounts.views import create_account_view, profile_view, change_default_times_view
from timer.views import index_view, editTask_view, add_points, deduct_points, is_logged_in, editUserSession_view

urlpatterns = [
    path('', index_view, name='index'),
    path('editTask/', editTask_view, name='editTask'),
    path('editUserSession/', editUserSession_view, name='editUserSession'),
    path('createaccount/', create_account_view, name='createaccount'),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="index.html"), name='logout'),
    path('admin/', admin.site.urls),
    path('profile/', profile_view, name='profile'),
    path('profile/change-default-times/', change_default_times_view,
         name='change-default-times'),
    path('addPoints/', add_points, name="addPoints"),
    path('deductPoints/', deduct_points, name="deductPoints"),
    path('isLoggedIn/', is_logged_in, name="isLoggedIn"),
]

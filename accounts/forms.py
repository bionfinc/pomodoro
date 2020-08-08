from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


# Extend the default signup form to include new fields
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')


class ChangeDefaultTimesForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['task_length', 'short_rest_length', 'long_rest_length']


class ChangeProfileInformationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

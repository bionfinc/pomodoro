from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Extend the default signup form to include new fields
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
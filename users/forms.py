from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Электронная почта')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', )

'''forms class for storing and logging in users'''
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    '''utilized for logging and testing if they have logged in'''
    username = forms.CharField(max_length=65, required=True)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput, required=True)


class RegisterForm(UserCreationForm):
    '''utilized to create users for registration'''
    email = forms.EmailField(required=True)

    class Meta:
        '''meta'''
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        '''ensures unique emails'''
        email = self.cleaned_data.get('email')
        # Check if the email already exists in the database
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

'''Forms module for user registration and login functionality'''

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    '''Form for user login.
    
    Fields:
        username (CharField): User's username, required for login.
        password (CharField): User's password, required for login, displayed as hidden input.
    '''
    username = forms.CharField(max_length=65, required=True)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput, required=True)


class RegisterForm(UserCreationForm):
    '''Form for user registration with email validation.

    Inherits:
        UserCreationForm: Base form for creating new users with password validation.

    Fields:
        email (EmailField): User's email, required for registration.

    Meta:
        model (User): User model for Django's built-in user system.
        fields (list): List of fields to include in the form: 
        'username', 'email', 'password1', 'password2'.
    '''
    email = forms.EmailField(required=True)

    class Meta:
        '''Meta options for RegisterForm, specifying model and fields.'''

        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        '''Validates email to ensure uniqueness.

        Raises:
            ValidationError: If the email is already associated with an existing account.
        
        Returns:
            str: The validated email if unique.
        '''
        email = self.cleaned_data.get('email')
        # Check if the email already exists in the database
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

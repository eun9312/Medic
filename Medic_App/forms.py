from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.core.validators import validate_email
from models import *

MAX_UPLOAD_SIZE = 2500000

# modified from class notes
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 30,
		    widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    firstname = forms.CharField(max_length = 30,
	    widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    lastname = forms.CharField(max_length = 30,
	    widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.CharField(max_length = 40, validators = [validate_email],
            widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',  
                                widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def clean_password2(self):
	password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")
        return username

    def clean_email(self):
	email = self.cleaned_data.get('email')
	if User.objects.filter(email__exact=email):
	    raise forms.ValidationError("Email is already in use.")
        return email

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))


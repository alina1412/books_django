from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import UsersManageModel

from django.contrib.auth.forms import UserCreationForm 


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="username", max_length=200,
               widget=forms.TextInput(attrs={"class":"form_field"}))

    password = forms.CharField(label="password", 
               widget=forms.PasswordInput(attrs={"class":"form_field"}))

    class Meta:
        model = UsersManageModel
        fields = ["username", "password"]


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="username", max_length=200,
               widget=forms.TextInput(attrs={"class":"form_field"}))

    password1 = forms.CharField(
        label="password",
        strip=False,
        widget=forms.PasswordInput(attrs={"class":"form_field",
        "autocomplete": "new-password"}))

    password2 = forms.CharField(
        label="password confirmation",
        widget=forms.PasswordInput(attrs={"class":"form_field",
        "autocomplete": "new-password"}),
        strip=False)
    # error_messages = UserCreationForm.error_messages
    # print(error_messages)

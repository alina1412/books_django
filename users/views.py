import logging

from users.models import UsersManageModel
logger = logging.getLogger(__name__)

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import LoginForm, RegisterForm
from shelves.models import Reader
from shelves.functions import FirstReaderCreation
# from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = settings.BASE_DIR


def shelves_user_creation(id, username):
    FirstReaderCreation.create_reader(id, username)


def login_user(request, user):
    login(request, user)
    messages.success(request, 'logged in')


def get_user_by_name(username):
    return User.objects.filter(username=username).first()


def get_or_create_demo_user():
    demo_username = 'demo_djando_user_for_books'
    demo_password = 'demo_user_password'
    user = get_user_by_name(demo_username)
    if not user:
        user = User.objects.create_user(
            username=demo_username, password=demo_password)
        user.save()
        shelves_user_creation(user.id, user.username)

    # create_demo_user_survey(user)
    return user


def home_view(request):
    context = {"auth": False}
    if request.user.is_authenticated:
        context = {"auth": True}
    else:
        if request.method == 'POST':
            user = get_or_create_demo_user()
            login_user(request, user)
            return HttpResponseRedirect(reverse('shelves:table_books'))
    return render(request, f'{BASE_DIR}/static/templates/home.html', context)


def delete_demo_user(request):
    if request.user.username == 'demo_djando_user_for_books':
        try:
            User.objects.filter(id=request.user.id).delete()
            Reader.objects.filter(name=request.user.username).delete()
        except Exception as e:
            print(e)


def logout_view(request):
    delete_demo_user(request)
    logout(request)
    # print('logged out')
    messages.success(request, 'logged out')
    return HttpResponseRedirect(reverse('users:home'))


def login_user_view(request):
    if request.user.is_authenticated:
        return redirect('users:home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'logged in')
            return redirect('shelves:table_books')
        messages.error(request, 'some error')
        return redirect('users:login_user')
    
    return render(request, f'{BASE_DIR}/static/templates/login_user.html', {'form': LoginForm()})



# from django.contrib.auth.forms import UserCreationForm 

def register_user(request):
    if request.user.is_authenticated:
        logout(request)
   
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        print("data:", username, password1, password2)
        
        form = RegisterForm(request.POST) # UserCreationForm(request.POST)
        if form.is_valid():
            print('valid')
            obj = form.save()
            print(obj, obj.id)
            shelves_user_creation(obj.id, username)
            messages.success(request, 'saved')
            return redirect('users:login_user')
        else:

            messages.error(request, 'some error')
    else:
        form = RegisterForm() # UserCreationForm()
    return render(request, 'templates/register.html', {'form': form}) 
    # return render(request, f'{BASE_DIR}/static/templates/register.html', {'form': form}) 


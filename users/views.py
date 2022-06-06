import logging

from users.models import UsersManageModel
logger = logging.getLogger(__name__)

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .forms import LoginForm, RegisterForm
from shelves.models import FirstReaderCreation
# from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = settings.BASE_DIR



def home_view(request):
    context = {"auth": False}
    if request.user.is_authenticated:
        context = {"auth": True}
    return render(request, f'{BASE_DIR}/static/templates/home.html', context)


def logout_view(request):
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




def shelves_user_creation(id, username):
    FirstReaderCreation.create_reader(id, username)

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


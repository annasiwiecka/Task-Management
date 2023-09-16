from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import *
from .decorators import unauthenticated_user
from .models import *

# Create your views here.

def index(request):
    return render(request, "task_management/index.html")


@unauthenticated_user
def register(request):
    form = NewUserForm()
    
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Successful registration {username}!")
            return redirect("login")

    else:
        form = NewUserForm()

    return render(request, "task_management/register.html", {
                "register_form": form
                })

@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "Invalid username or password") 
        else:
            messages.info(request, "Invalid username or password")   

    form = AuthenticationForm()
    return render(request, "task_management/login.html", {
        "login_form" : form
    })



def logoutPage(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("login")

@login_required(login_url="login")
def home(request):
    return render(request, "task_management/home.html")

@login_required(login_url="login")
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')

    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, "task_management/profile.html", {
        "user_form": user_form,
        "profile_form": profile_form
        })

  
#@login_required(login_url="login")
def notification(request):
    return render(request, "task_management/notification.html")

#@login_required(login_url="login")
def team(request):
    return render(request, "task_management/team.html")

#@login_required(login_url="login")
def project(request):
    return render(request, "task_management/project.html")

#@login_required(login_url="login")
def my_task(request):
    return render(request, "task_management/my_task.html")

#@login_required(login_url="login")
def settingsPage(request):
    return render(request, "task_management/settings.html")


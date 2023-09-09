from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .forms import *

# Create your views here.

def index(request):
    return render(request, "task_management/index.html")

def register(request):
    form = NewUserForm()
    
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    return render(request, "task_management/register.html", {
                "register_form": form
                })

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username, password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return HttpResponseRedirect("/home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = AuthenticationForm()
    return render(request, "task_management/login.html", {
        "login_form" : form
    })

def home(request):
    return render(request, "task_management/home.html")

def logout(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return HttpResponseRedirect("task_management/index.html")
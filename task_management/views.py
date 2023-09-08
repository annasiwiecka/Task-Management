from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from .forms import NewUserForm

# Create your views here.

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return HttpResponseRedirect("/login")
        else:
            messages.error(request, "Unsuccessful registration.")
    form = NewUserForm()
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

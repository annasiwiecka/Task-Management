from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib import messages

from .forms import NewUserForm

# Create your views here.

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return HttpResponseRedirect("/home")
        messages.error(request, "Unsuccessful registration.")
    form = NewUserForm()
    return render(request, "task_management/register.html", {
            "register_form": form
        })

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
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

@login_required(login_url="login")
def team(request, team_id=None):
    if team_id is None:
        return render(request, 'task_management/team.html') 

    else:
        team = get_object_or_404(Team, id=team_id)
    
    return render(request, 'task_management/team_id.html', {'team': team})

#@login_required(login_url="login")
def project(request):
    return render(request, "task_management/project.html")

#@login_required(login_url="login")
def my_task(request):
    return render(request, "task_management/my_task.html")

#@login_required(login_url="login")
def settingsPage(request):
    return render(request, "task_management/settings.html")

@login_required(login_url="login")
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.owner = request.user  # Set the owner to the current user
            team.save()
            return redirect('team_id', team_id=team.id)
    else:
        form = TeamForm()
    return render(request, 'task_management/create_team.html', {'form': form})

def list_all_teams(request):
    teams = Team.objects.all()
    return render(request, 'task_management/team.html', {"teams": teams})  

@login_required(login_url="login")
def sent_invitation(request):
    if request.method == 'POST':
        form = TeamInvitationForm(request.POST)
        if form.is_valid():
            invitation = form.save(commit=False)
            invitation.sender = request.user

            current_team = Team.objects.filter(members=request.user).first()
            if current_team:
                invitation.team = current_team

            invitation.save()
            Notification.objects.create(user=invitation.recipient, team_invitation=invitation, message="You've received a team invitation.")

            return redirect('invitation_sent')  # Redirect to a confirmation page
    else:
        form = TeamInvitationForm()

    return render(request, 'send_invitation.html', {'form': form})
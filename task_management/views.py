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
    return render(request, "task_management/notifications.html")

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
    return render(request, 'task_management/team_id.html', {"teams": teams}) 

def team_member(request, team_member_id):
    team_member = get_object_or_404(TeamMember, id=team_member_id)
    return render(request, 'team_member.html', {'team_member': team_member}) 

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
            recipient = invitation.receiver
            custom_message = f"You've received a team invitation from {invitation.sender.username} to join the team {invitation.team.name}. <a href='{invitation.get_absolute_url()}'>Click here</a> to view the invitation."
            link_url = invitation.get_absolute_url()
            Notification.objects.create(user=invitation.recipient, team_invitation=invitation, message="You've received a team invitation.")

            return redirect('invitation_sent')  
    else:
        form = TeamInvitationForm()

    return render(request, 'send_invitation.html', {'form': form})

def invitation_detail(request, invitation_id):
    invitation = get_object_or_404(TeamInvitation, pk=invitation_id)
    return render(request, 'invitation_detail.html', {'invitation': invitation})

def notification(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': notifications})

def accept_invitation(request, invitation_id):
    invitation = TeamInvitation.objects.get(pk=invitation_id)

    if request.method == 'POST':
        invitation.is_accepted = True
        invitation.save()

        team_member, created = TeamMember.objects.get_or_create(
            user=request.user,
            team=invitation.team,
            defaults={'role': 'Member'}  # You can customize the role as needed
        )

        team_member.is_active = True
        team_member.save()

        custom_message = f"{request.user.username} accepted your team invitation to join the team {invitation.team.name}. <a href='{invitation.get_absolute_url()}'>Click here</a> to view the invitation."
        link_url = invitation.get_absolute_url()
        Notification.objects.create(user=invitation.sender, custom_message=custom_message, link_url=link_url)


        # Redirect to the team's page or a confirmation page
        messages.success(request, f"You've joined {invitation.team.name} team!")
        return redirect('team_id', team_id=invitation.team.id)

    return render(request, 'accept_invitation.html', {'invitation': invitation})

def decline_invitation(request, invitation_id):
    invitation = get_object_or_404(TeamInvitation, pk=invitation_id)

    if request.method == 'POST':
        invitation.delete()

        decline_message = f"{request.user.username} declined your team invitation to join the team {invitation.team.name}."
        Notification.objects.create(user=invitation.sender, message=decline_message)

        messages.info(request, "You've declined the team invitation.")
        return redirect('notifications')

    return render(request, 'invitation.html', {'invitation': invitation})

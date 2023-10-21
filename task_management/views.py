from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
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

  
@login_required(login_url="login")
def notification(request):
    
    return render(request, "task_management/notifications.html")

@login_required(login_url="login")
def team(request, team_id):
    
    team = get_object_or_404(Team, id=team_id)
    team_members = TeamMember.objects.filter(team=team)
    
    current_team = None
    user_profile = UserCreate.objects.filter(user=request.user).first()
    
    if user_profile:
        current_team = user_profile.current_team
    

    return render(request, 'task_management/team_id.html', {
        'team': team,
        'team_members': team_members,
        'current_team': current_team
        })

@login_required(login_url="login")
def project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    tasks = Task.objects.filter(project=project)

    
    return render(request, "task_management/project.html", {
        'project': project,
        'tasks': tasks
    })
    

@login_required(login_url="login")
def my_task(request):
    return render(request, "task_management/my_task.html")

@login_required(login_url="login")
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
    return render(request, 'task_management/create_team.html', {
        'form': form
        })


@login_required(login_url="login")
def list_members(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    team_members = TeamMember.objects.filter(team=team)
    
    return render(request, 'task_management/list_team_members.html', {
        'team_members': team_members
        })

@login_required(login_url="login")
def team_member(request, team_member_id):
    team_member = get_object_or_404(TeamMember, id=team_member_id)
    is_owner = Team.objects.filter(owner=request.user, id=team_member.team.id).exists()
    

    can_edit_profile = (
        is_owner
        or request.user.has_perm('task_management.can_manage_team')  # Check the can_manage_team permission
    )
    
    
    return render(request, 'task_management/team_member.html', {
        'team_member': team_member,
        'can_edit_profile': can_edit_profile
        })
    
@login_required(login_url="login")
def team_member_edit(request, team_member_id):
    team_member = get_object_or_404(TeamMember, id=team_member_id)

    is_owner = Team.objects.filter(owner=request.user, id=team_member.team.id).exists()

    can_edit_profile = (
        is_owner
        or request.user.has_perm('task_management.can_manage_team')
    )

    if not can_edit_profile:
        return redirect('team_member', team_member_id=team_member_id)

    if request.method == 'POST':
        form = TeamMemberForm(request.POST, instance=team_member)
        if form.is_valid():
            
            if is_owner and form.cleaned_data.get('is_manager'):
                form.instance.role = 'Manager'
            elif is_owner:
                form.instance.role = 'Member'
            
            form.save()
            return redirect('team_member', team_member_id=team_member_id)
    else:
        form = TeamMemberForm(instance=team_member)
    return render(request, 'task_management/team_member_edit.html', {
        'team_member': team_member,
        'form': form,
        'can_edit_profile': can_edit_profile
    })

def team_member_delete(request, team_member_id):
    team_member = get_object_or_404(TeamMember, id=team_member_id)

    is_owner = request.user == team_member.user

    can_delete = (
        is_owner
        or request.user.has_perm('task_management.can_manage_team')
    )

    if not can_delete:
        return redirect('team_id', team_id=team.id)

    if request.method == 'POST':
        # Delete the team member upon confirmation
        team_member.delete()
        return redirect('team_id', team_id=team.id)

    return render(request, 'task_management/team_member_delete.html', {
        'team_member': team_member,
        'can_delete': can_delete
    })

@login_required(login_url="login")
def send_invitation(request):
    current_team = Team.objects.filter(owner=request.user).first()
    if current_team:

        if request.method == 'POST':
            form = TeamInvitationForm(request.POST)
            if form.is_valid():
                 
                invitation = form.save(commit=False)
                invitation.sender = request.user
                invitation.receiver = form.cleaned_data['receiver']

                if request.user == current_team.owner:
                    invitation.team = current_team
                    invitation.save()
                    messages.success(request, "You've sent a team invitation.")
                    

                    Notification.objects.create(user=invitation.receiver, team_invitation=invitation)
                    return redirect('send_invitation')
                else:
                    return HttpResponseForbidden("You are not the owner and cannot send invitations.")
            
                form = TeamInvitationForm()
        else:
            form = TeamInvitationForm()

    return render(request, 'task_management/send_invitation.html', {
        'form': form
        })

@login_required(login_url="login")
def invitation(request, invitation_id):
    invitation = get_object_or_404(TeamInvitation, pk=invitation_id)
    return render(request, 'task_management/invitation.html', {
        'invitation': invitation
        })

@login_required(login_url="login")
def notification(request):
    num_notifications = Notification.objects.count()
    user = request.user 
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'task_management/notification.html', {
        'notifications': notifications,
        'num_notifications': num_notifications
        })

def get_notification_count(request, team_member_id):
    team_member = get_object_or_404(TeamMember, id=team_member_id)

    count = Notification.objects.count()
    data = {'count': count}
    return JsonResponse(data)

def get_pending_project(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    count_in_progress = Project.objects.filter(team=team, status='In Progress').count()
    count_planning = Project.objects.filter(team=team, status='Planning').count()
    
    total_pending = count_planning + count_in_progress

    data = {'count': total_pending}
    return JsonResponse(data)

def get_total_projects(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    count = Project.objects.filter(team=team).count()
    data = {'count': count}
    return JsonResponse(data)

def get_complete_projects(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    count = Project.objects.filter(team=team, status='Completed')
    data = {'count': count}
    return JsonResponse(data)

@login_required(login_url="login")
def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(TeamInvitation, pk=invitation_id)

    if request.method == 'POST':
        invitation.is_accepted = True
        invitation.save()
        team_member, created = TeamMember.objects.get_or_create(
            user=request.user,
            team=invitation.team,
            defaults={'role': 'Member'}
        )
      
        TeamMember.objects.filter(user=request.user, team=invitation.team).update(is_active=False)

        team_member.is_active = True
        team_member.save()
        
        invitation.delete()

        messages.success(request, f"You've joined {invitation.team.name} team!")

    return redirect('team_id', team_id=invitation.team.id)

 
@login_required(login_url="login")
def decline_invitation(request, invitation_id):
    invitation = get_object_or_404(TeamInvitation, pk=invitation_id)


    if request.method == 'POST':
        invitation.delete()

        decline_message = f"{request.user.username} declined your team invitation to join the team {invitation.team.name}."
        Notification.objects.create(user=invitation.sender, message=decline_message)

        messages.info(request, "You've declined the team invitation.")
    return redirect('notification')


def create_project(request, team_id): 
    team = get_object_or_404(Team, id=team_id)
    
    if request.method == 'POST':
        form = ProjectForm(team=team, data=request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            
            project.save()
            project.team.add(team)
            
            return redirect('team_id', team_id)
    else:
        form = ProjectForm(team=team)

    return render(request, 'task_management/create_project.html', {
        'form': form,
        'team': team
    })

def create_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    team = project.team.all().first()
    if request.method == 'POST':
        form = TaskForm(request.POST, team=team)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.start = project.start 
            task.save()
            
            return redirect('project', project_id)
    else:
        form = TaskForm(team=team)
    return render(request, 'task_management/create_task.html', {
        'form': form,
        'project': project
    })

def project_board(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    projects = Project.objects.filter(team=team)  
       

    
    is_owner = team.owner == request.user
    
    can_create_project = (
        is_owner
        or request.user.has_perm('task_management.can_manage_team')  # Check the can_manage_team permission
    )
    num_pending_project = Project.objects.filter(status='In Progress').count()
    num_complete_projects =  Project.objects.filter(status='Completed').count()
    num_total_projects = Project.objects.filter(team=team).count()
    return render(request, 'task_management/project_board.html', {
        'projects': projects,
        'team': team,
  
        'num_total_projects': num_total_projects,
        'num_complete_projects': num_complete_projects,
        'num_pending_project': num_pending_project,
        'can_create_project': can_create_project,
    })

def list_tasks(request):
    pass


def task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    return render(request, 'task_management/task.html', {
        'task': task
    })
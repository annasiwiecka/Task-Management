from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import *


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']

class UpdateProfileForm(forms.ModelForm):
    name = forms.CharField()
    profile_picture = forms.ImageField()

    class Meta:
        model = UserCreate
        fields = ['name', 'profile_picture']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start', 'end', 'status']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to', 'deadline', 'priority', 'status']

class PriorityForm(forms.ModelForm):
    class Meta:
        model = Priority
        fields = '__all__'

class CommentForm(forms.ModelForm):
    model = Comment
    fields = ['content']
    
class Notification(forms.ModelForm):
    model = Notification
    fields = ['message', 'is_read']

class TeamInvitationForm(forms.ModelForm):
    class Meta:
        model = TeamInvitation
        fields = ['receiver', 'message']
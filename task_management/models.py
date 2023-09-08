from django.db import models


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    profile_picture = models.CharField(max_length=200, null=True)
    role = models.CharField(max_length=20)
    status = models.CharField(max_length=15)
    USERNAME_FIELD = "username"

class Team(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(2400)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_created")
    member = models.ForeignKey(User, on_delete=models.PROTECT, related_name="team_member")
    

class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=2400)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    status = models.CharField(max_length=20)

class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2400)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateTimeField()
    priority = models.CharField(max_length=30)
    status = models.CharField(max_length=15)

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    created_at = models.DateTimeField()

class Attachment(models.Model):
    file_name = models.CharField(max_length=40)
    file = models.CharField(max_length=200)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    upload = models.DateTimeField()

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    is_read = models.CharField(max_length=10)
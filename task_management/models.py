from django.db import models
from django.contrib.auth.models import User, Group
from PIL import Image


# Create your models here.

class UserCreate(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=30, null=True)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_images', blank=True)
    role = models.CharField(max_length=20, null=True)
    
    
    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super(UserCreate, self).save(*args, **kwargs)


        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)
   

class Team(models.Model):
    name = models.CharField(max_length=100, null=True)
    description = models.CharField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_created")
    members = models.ManyToManyField(User, related_name="team_member")
    
class CustomTeam(Group):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)



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


from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
    profile_picture = models.CharField(max_length=200, null=True)
    role = models.CharField(max_length=20)
    status = models.CharField(max_length=15)
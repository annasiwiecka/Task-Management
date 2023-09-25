from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import *

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserCreate.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=Team)
def create_team_member(sender, instance, created, **kwargs):
    if created:
        if instance.is_accepted:
            TeamMember.objects.create(user=instance.recipient, team=instance.team)
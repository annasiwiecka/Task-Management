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


@receiver(post_save, sender=TeamInvitation)
def create_team_member(sender, instance, created, **kwargs):
    if created and isinstance(instance, TeamInvitation) and instance.is_accepted:
        # Deactivate the existing TeamMember if it exists for the same user and team
        TeamMember.objects.filter(user=instance.receiver, team=instance.team).update(is_active=False)
        
        team_member, created = TeamMember.objects.get_or_create(user=instance.receiver, team=instance.team)
        team_member.is_active = True  # Make sure to set is_active to True
        
        if not team_member.user_profile:
            user_create_profile, created = UserCreate.objects.get_or_create(user=instance.receiver)
            team_member.user_profile = user_create_profile
        else:
            team_member.user_profile = instance.receiver.profile  # Assuming the correct related name is 'profile'
        
        team_member.save()
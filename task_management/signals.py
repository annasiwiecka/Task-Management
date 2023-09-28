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

'''@receiver(post_save, sender=TeamInvitation)
def create_team_member(sender, instance, created, **kwargs):
    if created and isinstance(instance, TeamInvitation) and instance.is_accepted:
        # Deactivate the existing TeamMember if it exists for the same user and team
        TeamMember.objects.filter(user=instance.receiver, team=instance.team).update(is_active=False)
        
        # Create the new TeamMember
        TeamMember.objects.create(user=instance.receiver, team=instance.team, is_active=True)'''

'''@receiver(post_save, sender=TeamInvitation)
def create_team_member(sender, instance, created, **kwargs):
    if created and isinstance(instance, TeamInvitation) and instance.is_accepted:
        # Deactivate the existing TeamMember if it exists for the same user and team
        existing_team_member = TeamMember.objects.filter(user=instance.receiver, team=instance.team).first()
        if existing_team_member:
            print(f"Deactivating existing TeamMember: {existing_team_member}")
            existing_team_member.is_active = False
            existing_team_member.save()
        
        # Create the new TeamMember
        new_team_member, created = TeamMember.objects.get_or_create(user=instance.receiver, team=instance.team)
        if created:
            print(f"Created new TeamMember: {new_team_member}")
        else:
            print(f"Using existing TeamMember: {new_team_member}")
        
        new_team_member.is_active = True
        new_team_member.save()'''
@receiver(post_save, sender=TeamInvitation)
def create_team_member(sender, instance, created, **kwargs):
    if created and isinstance(instance, TeamInvitation) and instance.is_accepted:
        # Deactivate the existing TeamMember if it exists for the same user and team
        TeamMember.objects.filter(user=instance.receiver, team=instance.team).update(is_active=False)
        
        # Create the new TeamMember
        TeamMember.objects.create(user=instance.receiver, team=instance.team, is_active=True)
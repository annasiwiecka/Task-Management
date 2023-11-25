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
        TeamMember.objects.filter(user=instance.receiver, team=instance.team).update(
            is_active=False
        )
        TeamMember.objects.create(
            user=instance.receiver, team=instance.team, is_active=True
        )


@receiver(post_save, sender=Project)
def update_project_status(sender, instance, **kwargs):
    if instance.status == "Completed":
        project = instance.project
        if project.calculate_overall_progress() == 100:
            project.status = "Completed"
            project.save()

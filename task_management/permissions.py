from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Team, TeamMember

can_manage_team = Permission.objects.create(
    codename='can_manage_team',
    name='Can manage team',
    content_type=ContentType.objects.get_for_model(Team),
)

can_manage_tasks = Permission.objects.create(
    codename='can_manage_tasks',
    name='Can manage tasks',
    content_type=ContentType.objects.get_for_model(Team),
)

team_owner_permission = Permission.objects.get(codename='can_manage_team')
manager_permission = Permission.objects.get(codename='can_manage_team')

for team in Team.objects.all():
    team.owner.user_permissions.add(team_owner_permission, manager_permission)


for team_member in TeamMember.objects.filter(is_manager=True):
    team_member.user.user_permissions.add(manager_permission)
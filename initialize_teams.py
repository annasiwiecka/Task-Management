from task_management.models import Team

def create_placeholder_team():
    team, created = Team.objects.get_or_create(
        id=0,  # Set a predefined ID
        defaults={'name': 'No Teams Available'}
    )

if __name__ == "__main__":
    create_placeholder_team()
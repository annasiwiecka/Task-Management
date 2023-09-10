from django.contrib import admin

# Register your models here.

from .models import UserTeam, Team, Project, Task, Comment, Attachment, Notification

admin.site.register(UserTeam)
admin.site.register(Team)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Attachment)
admin.site.register(Notification)

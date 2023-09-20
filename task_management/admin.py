from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(UserCreate)
admin.site.register(Team)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Attachment)
admin.site.register(Notification)
admin.site.register(TeamMember)
admin.site.register(Priority)
admin.site.register(Message)
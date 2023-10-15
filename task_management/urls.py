from django.urls import path 
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    
    path("register/", views.register, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout", views.logoutPage, name="logout"),
    
    path("home", views.home, name="home"),
    
   path("profile/", views.profile, name="profile"),
   path("notification", views.notification, name="notification"),
   path("team/<int:team_id>/", views.team, name="team_id"),
   path("project", views.project, name="project"),
   path("my-task", views.my_task, name="my-task"),
   path("Settings", views.settingsPage, name="settings"),
   path("teams/", views.list_all_teams, name="list"),

   path("create-team", views.create_team, name="create_team"),
   path("send_invitation", views.send_invitation, name="send_invitation"),
   path("invitation/<int:invitation_id>/", views.invitation, name="invitation"),
   path("accept_invitation/<int:invitation_id>/", views.accept_invitation, name="accept_invitation"),
   path("decline_invitation/<int:invitation_id>/", views.decline_invitation, name="decline_invitation"),

    path('team_member/<int:team_member_id>/', views.team_member, name="team_member"),
    path('team_member/<int:team_member_id>/edit/', views.team_member_edit, name="team_member_edit"),
    path('team_member/<int:team_member_id>/delete', views.team_member_delete, name="team_member_delete"),
    path('create_project', views.create_project, name="create_project"),
    path('get_notification_count/', views.get_notification_count, name='get_notification_count'),

    #path('create_task', views.)
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
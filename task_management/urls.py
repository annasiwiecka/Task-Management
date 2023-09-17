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
   path("team/'", views.team, name="team"),
   path('team/<int:team_id>/', views.team, name='team_with_id'),
   path("project", views.project, name="project"),
   path("my-task", views.my_task, name="my-task"),
   path("Settings", views.settingsPage, name="settings"),

   path("create-team", views.create_team, name="create_team")
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
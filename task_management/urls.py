from django.urls import path 
from . import views

urlpatterns = [
    path(""),
    path("register/", views.register, name="register"),
    path("login/")
]
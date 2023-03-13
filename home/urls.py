from django.urls import path

from . import views

urlpatterns = [
    path("", views.unauthhome, name="home"),
    path("home/", views.home, name="authorisedhome"),
    path("login/", views.loginpage, name="login"),
    path("logout/", views.logoutuser, name="logout"),
    path("register/", views.register, name="register"),
]
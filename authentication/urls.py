from django.urls import path
from .views import login, dashboard, register

urlpatterns = [
    path("", login, name="home"),
    path("login/", login, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("register/", register, name="register"),
]
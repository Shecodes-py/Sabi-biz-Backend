from django.urls import path
from .views import login_view, dashboard, register, logout_view

urlpatterns = [
    path("", login_view, name="home"),
    path("login_view/", login_view, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("register/", register, name="register"),
    path("logout/", logout_view, name="logout"),
]
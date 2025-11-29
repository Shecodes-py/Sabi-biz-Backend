from django.urls import path
from .views import *

urlpatterns = [
    path("", login_view, name="home"),
    path("login_view/", login_view, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("register/", register, name="register"),
    path("logout/", logout_view, name="logout"),
    path("add_sale/", add_sale, name="add_sale"),
    path("add_expense/", add_expense, name="add_expense"),

]
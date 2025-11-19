# from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 

# Create your views here.

# login
def login(request):
    if request.method == "POST":
        email = request.POST.get("email") 
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Login successful")
        else:
            return HttpResponse("Invalid credentials")
    return HttpResponse("Login Page")

# register
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists")
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return HttpResponse("Registration successful")
    return HttpResponse("Register page")

# dashboard
@login_required
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_URL)
    return HttpResponse("Dashboard page")
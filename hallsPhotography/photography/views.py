from django.shortcuts import render, redirect
from django.contrib.auth import logout
# Create your views here.
from django.shortcuts import render
from .authenticate_user import *
from django.views.decorators.csrf import csrf_protect

def login(request):
    if request.method == "POST":
        user_object = {
            "username": request.POST["username"],
            "password": request.POST["password"],
        }
        authetnicate_user(request, user_object)
    if request.user.is_authenticated:
        return redirect("home")
    else:
        return render(request, 'login.html')

def sign_up(request):
    if request.method == "POST":
        user_object = {
            "email": request.POST["email"],
            "username": request.POST["username"],
            "password": request.POST["password"],
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"]
        }
        db_sign_up(user_object)
        authetnicate_user(request, user_object)
        
    if request.user.is_authenticated:
        return redirect("home")
    else:
        return render(request, 'signup.html')

@csrf_protect
def home(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    if request.user.is_authenticated:
        return render(request, 'main.html')
    else:
        return redirect("login")
from django.shortcuts import render, redirect
from django.contrib.auth import logout, get_user_model
# Create your views here.
from django.shortcuts import render
from .authenticate_user import *
from django.views.decorators.csrf import csrf_protect
from photography.s3 import S3Storage
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

def home(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    user = False
    if request.user.is_authenticated:
        username = request.user
        User = get_user_model()
        user = User.objects.get(username=username)
        
    return render(request, 'home.html', context={
        "request": request,
        "user": user,
    })

def login(request):
    if request.method == "POST":
        user_object = {
            "username": request.POST["username"],
            "password": request.POST["password"],
        }
        authetnicate_user(request, user_object)
    if request.user.is_authenticated:
        return redirect("profile")
    else:
        return render(request, 'login.html')

def download(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "download_file.html")
        elif request.method == "POST":
            file_name = "new_test.jpg"
            bucket = "portfoliophotographs"
            s3_file = S3Storage(file_name=file_name, bucket=bucket)
            return s3_file.download_file()
    return redirect("login")




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
        return redirect("profile")
    else:
        return render(request, 'signup.html')

@csrf_protect
def profile(request):
    username = request.user
    User = get_user_model()
    user = User.objects.get(username=username)
    if request.method == "POST":
        logout(request)
        return redirect("home")
    if request.user.is_authenticated:
        return render(request, 'main.html', context={"request": request, "user": user})
    else:
        return redirect("login")
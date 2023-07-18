from django.shortcuts import render, redirect
from django.contrib.auth import logout, get_user_model
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .authenticate_user import *
from photography.s3 import S3Storage
from rest_framework.decorators import api_view
import tempfile
from django.http import JsonResponse
from photography.dependencies import get_database
from photography.crud.package import create_database_package

def home(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    
    user = False
    if request.user.is_authenticated:
        User = get_user_model()
        user = User.objects.get(username=request.user)
        
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

def upload(request):
    if request.user.is_authenticated:
        if request.method == "POST" and 'upload' in request.FILES:
            file = request.FILES['upload']
            s3_storage = S3Storage(file.name, 'packagephotos')
            with tempfile.NamedTemporaryFile() as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)
                temp_file.flush()
                s3_storage.upload_file(temp_file.name)
            return redirect("upload")
        return render(request, "upload_file.html")
    return render(request, 'login.html')

def download(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "download_file.html")
        elif request.method == "POST":
            file_name = "Jira.csv"
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
        authenticate_user(request, user_object)
        
    if request.user.is_authenticated:
        return redirect("profile")
    else:
        return render(request, 'signup.html')

@csrf_protect
def profile(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    
    User = get_user_model()
    user = User.objects.get(username=request.user)
    
    if request.user.is_authenticated:
        return render(request, 'main.html', context={"request": request, "user": user})
    else:
        return redirect("login")


def create_package(request):
    if request.user.is_authenticated:
        User = get_user_model()
        user = User.objects.get(username=request.user)
        if request.method == 'POST':
            name = request.POST.get('name')
            time_frame = request.POST.get('time_frame')
            price = float(request.POST.get('price'))

            # Get a database session
            database = get_database()

            # Create the database package
            database_package = create_database_package(database, name, time_frame, price)
            file = request.FILES['upload']
            s3_storage = S3Storage(file.name, 'packagephotos')
            with tempfile.NamedTemporaryFile() as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)
                temp_file.flush()
                s3_storage.upload_file(temp_file.name)

            return JsonResponse({
                'name': database_package.name,
                'time_frame': database_package.time_frame,
                'price': database_package.price
            })
        else:
            return render(request, 'create_package.html', context={
                "request": request,
                "user": user
            })
    return redirect('login')
from django.shortcuts import render, redirect
from django.contrib.auth import logout, get_user_model
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .authenticate_user import *
from photography.s3 import S3Storage
from rest_framework.decorators import api_view
import tempfile
from django.http import JsonResponse
from photography.dependencies import get_database
from photography.crud.package import (
    create_database_package,
    get_all_database_packages,
    delete_db_package_by_package_id,
)
from functools import wraps


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")  # Redirect to your login page

        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
def packages(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")

    user = False

    User = get_user_model()
    user = User.objects.get(username=request.user)
    database = get_database()
    database_packages = get_all_database_packages(database=database)
    for package in database_packages:
        if package.file_name:
            init_photo = S3Storage(bucket="packagephotos", file_name=package.file_name)
            package.photo = init_photo.get_photo()

    return render(
        request,
        "packages.html",
        context={"request": request, "user": user, "packages": database_packages},
    )


def home(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, "home.html")
    return redirect("login")


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
        return render(request, "login.html")


@login_required
def upload(request):
    if request.method == "POST" and "upload" in request.FILES:
        file = request.FILES["upload"]
        s3_storage = S3Storage(file.name, "packagephotos")
        with tempfile.NamedTemporaryFile() as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file.flush()
            s3_storage.upload_file(temp_file.name)
        return redirect("upload")
    return render(request, "upload_file.html")


@login_required
def download(request):
    if request.method == "GET":
        return render(request, "download_file.html")
    elif request.method == "POST":
        file_name = "Jira.csv"
        bucket = "portfoliophotographs"
        s3_file = S3Storage(file_name=file_name, bucket=bucket)
        return s3_file.download_file()


def sign_up(request):
    if request.method == "POST":
        user_object = {
            "email": request.POST["email"],
            "username": request.POST["username"],
            "password": request.POST["password"],
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
        }
        db_sign_up(user_object)
        authenticate_user(request, user_object)

    if request.user.is_authenticated:
        return redirect("profile")
    else:
        return render(request, "signup.html")


@login_required
def profile(request):
    if request.method == "POST":
        logout(request)
        return redirect("packages")

    User = get_user_model()
    user = User.objects.get(username=request.user)
    return render(request, "main.html", context={"request": request, "user": user})


@login_required
def create_package(request):
    User = get_user_model()
    user = User.objects.get(username=request.user)
    if request.method == "POST":
        if "logout" in request.POST:
            logout(request)
            return redirect("login")

        if (
            "form_type" in request.POST
            and request.POST["form_type"] == "create_package"
        ):
            name = request.POST.get("name")
            time_frame = request.POST.get("time_frame")
            price = request.POST.get("price")

            if price is not None and price.strip():
                try:
                    price = float(price)
                except ValueError:
                    return HttpResponse("Invalid price value")

                file = request.FILES["upload"]
                file_name = file.name

                # Get a database session
                database = get_database()

                # Create the database package
                database_package = create_database_package(
                    database, name, time_frame, price, file_name
                )
                s3_storage = S3Storage(file_name, "packagephotos")
                s3_storage.upload_file(file)

                return JsonResponse(
                    {
                        "name": database_package.name,
                        "time_frame": database_package.time_frame,
                        "price": database_package.price,
                    }
                )

    return render(
        request,
        "create_package.html",
        context={"request": request, "user": user},
    )

import os
import sys
from django.contrib.auth import authenticate, login, logout
import django
from photography.models import User

# Add the project directory to Python path
project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_directory)

# Replace 'hallsPhotography' with your actual project name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hallsPhotography.settings')
django.setup()


def authetnicate_user(request, user):
    user = authenticate(username=user["username"], password=user["password"])
    # logout(request)
    if user is not None:
        login(request, user)
        print(user)
        print("Authentication successful")
    else:
        print("Authentication failed")



# from django.contrib.auth.models import User


# Create user and save to the database
def db_sign_up(user):
    username = user["username"]
    email = user["email"]
    password = user["password"]
    first_name = user["first_name"]
    last_name = user["last_name"]
    user = User.objects.create_user(username, email, password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

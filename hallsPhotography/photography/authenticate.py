import os
import sys
from django.contrib.auth import authenticate
import django

# Add the project directory to Python path
project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_directory)

# Replace 'hallsPhotography' with your actual project name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hallsPhotography.settings')
django.setup()


def authetnicate_user(user):
    user = authenticate(username=user["username"], password=user["password"])
    if user is not None:
        print("Authentication successful")
    else:
        print("Authentication failed")
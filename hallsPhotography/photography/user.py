import os
import sys

# Add the project directory to Python path
project_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_directory)

# Set up Django
import django

# Replace 'hallsPhotography' with your actual project name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hallsPhotography.settings')
django.setup()

# from django.contrib.auth.models import User
from photography.models import User

# Create user and save to the database
user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')

# Update fields and then save again
user.first_name = 'Tyrone'
user.last_name = 'Citizen'
user.save()

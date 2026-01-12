import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrishtiPlatform.settings')
django.setup()

User = get_user_model()

users_to_create = [
    {'username': 'citizen', 'password': '123', 'role': 'citizen'},
    {'username': 'officer', 'password': '123', 'role': 'officer'},
]

for user_data in users_to_create:
    username = user_data['username']
    password = user_data['password']
    role = user_data['role']

    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.role = role
        user.save()
        print(f"Successfully updated user '{username}' with password '{password}' and role '{role}'.")
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, password=password)
        user.role = role
        user.save()
        print(f"Successfully created user '{username}' with password '{password}' and role '{role}'.")
    except Exception as e:
        print(f"Error processing user '{username}': {e}")

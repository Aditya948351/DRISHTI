import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrishtiPlatform.settings')
django.setup()

User = get_user_model()
username = 'admin'
password = '123'
role = 'super_admin'

try:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.role = role
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"Successfully updated user '{username}' with password '{password}' and role '{role}'.")
except User.DoesNotExist:
    user = User.objects.create_user(username=username, password=password)
    user.role = role
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f"Successfully created user '{username}' with password '{password}' and role '{role}'.")
except Exception as e:
    print(f"Error: {e}")

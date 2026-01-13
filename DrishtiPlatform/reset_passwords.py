import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrishtiPlatform.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
password = "Aditya@123"

users = User.objects.all()
print(f"Resetting passwords for {users.count()} users to '{password}'...")

for user in users:
    user.set_password(password)
    user.save()
    print(f"User: {user.username} ({user.role}) - Password updated")

print("Done.")

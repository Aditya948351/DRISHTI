import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrishtiPlatform.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def fix_user():
    username = 'diksha_patil'
    try:
        u = User.objects.get(username=username)
        u.set_password('Drishti@123')
        u.is_active = True
        u.save()
        print(f"SUCCESS: Reset password for '{username}'.")
        print(f"Details -> Role: {u.role}, Active: {u.is_active}, ID: {u.id}")
    except User.DoesNotExist:
        print(f"ERROR: User '{username}' not found!")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    fix_user()

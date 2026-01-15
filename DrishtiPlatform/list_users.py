import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrishtiPlatform.settings')
django.setup()
from accounts.models import User

users = User.objects.all().order_by('role', 'username')

print(f"{'Username':<20} | {'Role':<20} | {'State':<15} | {'District':<15}")
print("-" * 80)
for user in users:
    print(f"{user.username:<20} | {user.get_role_display():<20} | {user.state or '-':<15} | {user.district or '-':<15}")

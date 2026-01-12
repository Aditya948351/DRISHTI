import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrishtiPlatform.settings')
django.setup()

from django.contrib.auth import get_user_model
from complaints.models import Complaint

User = get_user_model()

print("--- USERS & ROLES ---")
print(f"{'Username':<20} | {'Role':<15} | {'Password'}")
print("-" * 50)
for u in User.objects.all().order_by('role'):
    print(f"{u.username:<20} | {u.role:<15} | password123")

print("\n--- STATISTICS ---")
print(f"Total Citizens: {User.objects.filter(role='citizen').count()}")
print(f"Total Complaints: {Complaint.objects.count()}")

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrishtiPlatform.settings')
django.setup()
from accounts.models import User
from complaints.models import Complaint

print(f"Total Users: {User.objects.count()}")
print(f"Citizens: {User.objects.filter(role='citizen').count()}")
print(f"Officers: {User.objects.filter(role__in=['officer', 'city_admin', 'dept_admin']).count()}")
print(f"Complaints: {Complaint.objects.count()}")

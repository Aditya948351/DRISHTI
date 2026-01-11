from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from complaints.models import Department

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates dummy users for testing'

    def handle(self, *args, **kwargs):
        # Create Departments if they don't exist
        dept1, _ = Department.objects.get_or_create(name="Public Works", description="Roads and infrastructure")
        dept2, _ = Department.objects.get_or_create(name="Sanitation", description="Waste management")
        
        users = [
            {'username': 'citizen', 'password': '123', 'role': 'citizen'},
            {'username': 'officer', 'password': '123', 'role': 'officer', 'department': dept1},
            {'username': 'dept_admin', 'password': '123', 'role': 'dept_admin', 'department': dept1},
            {'username': 'state_admin', 'password': '123', 'role': 'city_admin'},
            {'username': 'national_admin', 'password': '123', 'role': 'super_admin'},
        ]

        for u in users:
            user, created = User.objects.get_or_create(username=u['username'])
            user.set_password(u['password'])
            user.role = u['role']
            if 'department' in u:
                user.department = u['department']
            user.save()
            self.stdout.write(self.style.SUCCESS(f"User {u['username']} ({u['role']}) ready"))

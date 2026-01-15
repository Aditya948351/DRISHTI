import os
import django
import random
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrishtiPlatform.settings')
django.setup()

from accounts.models import User
from complaints.models import Complaint, Department, Category

def create_data():
    print("Starting data population...")

    # Create Departments if they don't exist
    dept_names = ['Public Works', 'Health', 'Education', 'Police', 'Municipal Corporation']
    departments = []
    for name in dept_names:
        dept, created = Department.objects.get_or_create(name=name)
        departments.append(dept)
    print(f"Departments ensured: {[d.name for d in departments]}")

    # Create Categories
    categories = []
    cat_names = ['Potholes', 'Garbage Collection', 'Water Supply', 'Noise Pollution', 'Street Lights']
    for i, name in enumerate(cat_names):
        cat, created = Category.objects.get_or_create(name=name, department=departments[i % len(departments)])
        categories.append(cat)
    print(f"Categories ensured: {[c.name for c in categories]}")

    # Create Citizens
    citizens_data = [
        {'username': 'aarav_mh', 'first_name': 'Aarav', 'last_name': 'Patil', 'state': 'Maharashtra', 'email': 'aarav@example.com'},
        {'username': 'vihaan_mh', 'first_name': 'Vihaan', 'last_name': 'Deshmukh', 'state': 'Maharashtra', 'email': 'vihaan@example.com'},
        {'username': 'diya_gj', 'first_name': 'Diya', 'last_name': 'Patel', 'state': 'Gujarat', 'email': 'diya@example.com'},
        {'username': 'ishaan_gj', 'first_name': 'Ishaan', 'last_name': 'Shah', 'state': 'Gujarat', 'email': 'ishaan@example.com'},
        {'username': 'ananya_gj', 'first_name': 'Ananya', 'last_name': 'Mehta', 'state': 'Gujarat', 'email': 'ananya@example.com'},
    ]

    citizens = []
    for data in citizens_data:
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password='password123',
                first_name=data['first_name'],
                last_name=data['last_name'],
                role='citizen',
                state=data['state']
            )
            citizens.append(user)
            print(f"Created citizen: {user.username}")
        else:
            citizens.append(User.objects.get(username=data['username']))
            print(f"Citizen already exists: {data['username']}")

    # Create Officers
    officers_data = [
        {'username': 'officer_mh', 'role': 'city_admin', 'state': 'Maharashtra', 'first_name': 'Rajesh', 'last_name': 'Pawar'},
        {'username': 'officer_gj', 'role': 'city_admin', 'state': 'Gujarat', 'first_name': 'Suresh', 'last_name': 'Joshi'},
        {'username': 'local_officer', 'role': 'officer', 'state': 'Maharashtra', 'first_name': 'Amit', 'last_name': 'Singh'}, # Local officer
        {'username': 'dept_admin', 'role': 'dept_admin', 'state': 'Maharashtra', 'first_name': 'Priya', 'last_name': 'Sharma'}, # Other/Dept Admin
    ]

    for data in officers_data:
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create_user(
                username=data['username'],
                email=f"{data['username']}@example.com",
                password='password123',
                first_name=data['first_name'],
                last_name=data['last_name'],
                role=data['role'],
                state=data['state']
            )
            print(f"Created officer: {user.username} ({user.role})")
        else:
            print(f"Officer already exists: {data['username']}")

    # Create Complaints
    complaint_titles = [
        "Huge pothole on Main Road",
        "Garbage not collected for 3 days",
        "Low water pressure in colony",
        "Loud music from nearby hall late night",
        "Street light blinking continuously"
    ]

    for i, citizen in enumerate(citizens):
        # Create 1-2 complaints per citizen
        for j in range(random.randint(1, 2)):
            title = random.choice(complaint_titles)
            cat = random.choice(categories)
            dept = cat.department
            
            complaint = Complaint.objects.create(
                title=f"{title} - {citizen.username} {j+1}",
                description=f"This is a sample complaint description for {title}. Please resolve this issue.",
                citizen=citizen,
                category=cat,
                department=dept,
                location=f"Area {j+1}, {citizen.state}",
                status='new',
                priority='medium'
            )
            print(f"Created complaint: {complaint.title} for {citizen.username}")

    print("Data population completed successfully.")

if __name__ == '__main__':
    create_data()

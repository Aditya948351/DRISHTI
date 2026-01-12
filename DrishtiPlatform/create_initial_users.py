import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrishtiPlatform.settings')
django.setup()

from accounts.models import User
from complaints.models import Department

def create_users():
    # Ensure a default department exists
    dept, created = Department.objects.get_or_create(
        name="General Administration",
        defaults={'description': "Default department for initial officers"}
    )
    if created:
        print(f"Created Department: {dept.name}")

    users_data = [
        {
            'username': 'sakshi_rote',
            'first_name': 'Sakshi',
            'last_name': 'Rote',
            'role': 'dept_admin',
            'department': dept,
            'address': 'Department Admin Office'
        },
        {
            'username': 'sejal_thopate',
            'first_name': 'Sejal',
            'last_name': 'Thopate',
            'role': 'city_admin',
            'department': None, # State admins might not belong to a specific dept
            'address': 'Maharashtra'
        },
        {
            'username': 'diksha_patil',
            'first_name': 'Diksha',
            'last_name': 'Patil',
            'role': 'officer',
            'department': dept,
            'address': 'Local Ward Office'
        },
        {
            'username': 'dimpal_pardeshi',
            'first_name': 'Dimpal',
            'last_name': 'Pardeshi',
            'role': 'city_admin',
            'department': None,
            'address': 'Gujarat'
        }
    ]

    default_password = "Drishti@123"

    print("\n--- Creating Users ---")
    for data in users_data:
        username = data['username']
        if User.objects.filter(username=username).exists():
            print(f"User {username} already exists. Skipping.")
            user = User.objects.get(username=username)
            # Update role/address just in case
            user.role = data['role']
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.address = data['address']
            user.department = data['department']
            user.save()
            print(f"Updated {username}.")
        else:
            user = User.objects.create_user(
                username=username,
                email=f"{username}@drishti.gov.in",
                password=default_password,
                first_name=data['first_name'],
                last_name=data['last_name'],
                role=data['role'],
                department=data['department'],
                address=data['address']
            )
            print(f"Created User: {username} ({data['role']})")

    print("\n--- Credentials ---")
    print(f"Password for all accounts: {default_password}")
    for data in users_data:
        print(f"Role: {data['role']:<15} | Username: {data['username']}")

if __name__ == '__main__':
    create_users()

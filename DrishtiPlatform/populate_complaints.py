import os
import django
import random
from django.utils import timezone

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DrishtiPlatform.settings')
django.setup()

from django.contrib.auth import get_user_model
from complaints.models import Complaint, Category, Department

User = get_user_model()

def populate():
    # 1. Cleanup Incorrect Users/Data
    try:
        User.objects.filter(username__in=['Aditya', 'Siddhi']).delete()
    except:
        pass

    # 2. Get or Create Correct Users
    def get_or_create_user(username):
        user, created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@example.com', 'role': 'citizen'})
        if created:
            user.set_password('password123')
            user.save()
        return user

    aditya = get_or_create_user('Aditya948351')
    siddhu = get_or_create_user('siddhu123')

    # 3. Ensure Departments & Categories (6 Categories)
    dept_map = {
        'Water Board': ['Water Supply'],
        'Public Works': ['Roads & Transport', 'Electricity'],
        'Sanitation Dept': ['Sanitation'],
        'Traffic Police': ['Traffic'],
        'Police Dept': ['Public Safety']
    }
    category_objects = {}
    for dept_name, cats in dept_map.items():
        dept, _ = Department.objects.get_or_create(name=dept_name)
        for cat_name in cats:
            cat, _ = Category.objects.get_or_create(name=cat_name, defaults={'department': dept})
            category_objects[cat_name] = cat

    # 4. Define Data (Mixed Priorities for Sorting Demo)
    # Aditya948351: 3 Complaints
    aditya_data = [
        {"title": "Suspicious Activity in Park", "desc": "Group of people gathering late at night, looks unsafe.", "cat": "Public Safety", "loc": "Central Park", "prio": "critical"},
        {"title": "Streetlight Flickering", "desc": "Light causing distraction.", "cat": "Electricity", "loc": "Block B", "prio": "medium"},
        {"title": "Pothole on Main Road", "desc": "Small pothole but growing.", "cat": "Roads & Transport", "loc": "Main Market", "prio": "low"},
    ]

    # siddhu123: 6 Complaints
    siddhu_data = [
        {"title": "Major Pipe Burst", "desc": "Water flooding the street, urgent!", "cat": "Water Supply", "loc": "Sector 7", "prio": "critical"},
        {"title": "Traffic Signal Stuck Red", "desc": "Causing huge jam at crossing.", "cat": "Traffic", "loc": "Sector 7 Crossing", "prio": "high"},
        {"title": "Garbage Dump Overflow", "desc": "Smell is unbearable, health hazard.", "cat": "Sanitation", "loc": "Block D", "prio": "high"},
        {"title": "Illegal Parking Blocking Gate", "desc": "Cannot take car out.", "cat": "Traffic", "loc": "Market", "prio": "medium"},
        {"title": "Construction Debris", "desc": "Left on sidewalk.", "cat": "Roads & Transport", "loc": "Lane 5", "prio": "low"},
        {"title": "Stray Dog Aggression", "desc": "Chasing bikers.", "cat": "Public Safety", "loc": "School Road", "prio": "high"},
    ]

    # 5. Create Complaints
    def create_batch(user, data_list):
        # Clear existing to avoid dupes
        Complaint.objects.filter(citizen=user).delete()
        
        for data in data_list:
            cat = category_objects.get(data['cat'])
            Complaint.objects.create(
                citizen=user,
                title=data['title'],
                description=data['desc'],
                category=cat,
                department=cat.department,
                location=data['loc'],
                ai_predicted_category=data['cat'],
                ai_predicted_priority=data['prio'], # Using explicit priority for demo
                ai_confidence_score=random.uniform(85.0, 99.0),
                status='new',
                workflow_state='pending_verification',
                created_at=timezone.now()
            )
            print(f"Created: '{data['title']}' ({data['prio']})")

    print("\nPopulating Aditya948351...")
    create_batch(aditya, aditya_data)

    print("\nPopulating siddhu123...")
    create_batch(siddhu, siddhu_data)

    print("\nDone! Data refreshed with 6 categories and sorted priorities.")

if __name__ == '__main__':
    populate()

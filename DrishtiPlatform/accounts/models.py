from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('citizen', 'Citizen'),
        ('officer', 'Local Officer'),
        ('dept_admin', 'Department Admin'),
        ('city_admin', 'City/State Authority'),
        ('super_admin', 'System Super Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='citizen')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    department = models.ForeignKey('complaints.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='officers')
    
    # Extended Profile Fields
    STATE_CHOICES = (
        ('Maharashtra', 'Maharashtra'),
        ('Gujarat', 'Gujarat'),
    )
    state = models.CharField(max_length=50, choices=STATE_CHOICES, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True, help_text="District for Local Officers")
    aadhaar_number = models.CharField(max_length=12, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    
    # Profile Fields
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/citizen_<id>/<filename>
        return 'citizen_{0}/{1}'.format(instance.id, filename)

    profile_picture = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    
    # Gamification
    points = models.IntegerField(default=0)
    rank = models.CharField(max_length=50, default='Novice Citizen') # e.g., Novice, Active, Guardian, Hero, Legend

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

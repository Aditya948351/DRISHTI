from django.db import models
from django.conf import settings
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='categories')
    sla_hours = models.IntegerField(default=48, help_text="SLA in hours for resolution")

    def __str__(self):
        return self.name

class Complaint(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('ai_suggested', 'AI Triage Suggested'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed'),
    )
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    citizen = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='complaints')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_officer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints')
    
    WORKFLOW_CHOICES = (
        ('pending_verification', 'Pending Verification'),
        ('verified_by_officer', 'Verified by Officer'),
        ('forwarded_to_redressal', 'Forwarded to Redressal'),
        ('resolved', 'Resolved'),
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    workflow_state = models.CharField(max_length=50, choices=WORKFLOW_CHOICES, default='pending_verification', help_text="Current stage in approval workflow")
    is_verified = models.BooleanField(default=False, help_text="True if verified as a genuine issue")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    location = models.CharField(max_length=255, help_text="Area/Locality")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    attachment = models.FileField(upload_to='complaints/', null=True, blank=True)
    
    # Resolution Proof
    resolution_photo = models.ImageField(upload_to='resolutions/', null=True, blank=True)
    is_final_verified = models.BooleanField(default=False, help_text="True if local officer verifies the resolution")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    # AI Predictions (stored for reference/audit)
    ai_predicted_category = models.CharField(max_length=100, null=True, blank=True)
    ai_predicted_priority = models.CharField(max_length=20, null=True, blank=True)
    ai_confidence_score = models.FloatField(null=True, blank=True)
    
    # SLA
    sla_deadline = models.DateTimeField(null=True, blank=True)
    
    # Rejection
    rejection_reason = models.TextField(blank=True, null=True, help_text="Reason for rejection by officer")

    def __str__(self):
        return f"{self.title} ({self.status})"

class ComplaintActivity(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='activities')
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100) # e.g., "Status Updated", "Comment Added"
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} on {self.complaint} by {self.actor}"

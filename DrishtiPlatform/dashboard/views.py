from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from complaints.models import Complaint, Department
from community.models import DiscussionThread

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'citizen':
        return redirect('citizen_dashboard')
    elif user.role == 'officer':
        return redirect('officer_dashboard')
    elif user.role == 'dept_admin':
        return redirect('dept_dashboard')
    elif user.role == 'city_admin':
        return redirect('state_dashboard')
    elif user.role == 'super_admin':
        return redirect('national_dashboard')
    return redirect('home')

# Shared System Views
def shared_error(request):
    return render(request, 'SharedSystemPages/error.html')

def shared_redirect(request):
    return render(request, 'SharedSystemPages/redirect.html')

# Citizen Views
@login_required
def citizen_dashboard(request):
    if request.user.role != 'citizen':
        return redirect('dashboard')
    
    complaints = Complaint.objects.filter(citizen=request.user)
    stats = {
        'total': complaints.count(),
        'pending': complaints.exclude(status='resolved').count(),
        'resolved': complaints.filter(status='resolved').count(),
    }
    recent_complaints = complaints.order_by('-created_at')[:5]
    
    return render(request, 'Citizen/dashboard.html', {
        'stats': stats,
        'recent_complaints': recent_complaints
    })

@login_required
def citizen_submit_complaint(request):
    if request.user.role != 'citizen':
        return redirect('dashboard')
        
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        dept_id = request.POST.get('department')
        
        department = get_object_or_404(Department, id=dept_id)
        
        Complaint.objects.create(
            citizen=request.user,
            title=title,
            description=description,
            department=department,
            status='pending',
            workflow_state='local_pending' # Initial workflow state
        )
        
        # Gamification: Award points for lodging complaint
        request.user.points += 10
        request.user.save()
        
        return redirect('citizen_dashboard')
        
    departments = Department.objects.all()
    return render(request, 'Citizen/complaints.html', {'departments': departments})

@login_required
def citizen_my_complaints(request):
    if request.user.role != 'citizen':
        return redirect('dashboard')
    complaints = Complaint.objects.filter(citizen=request.user).order_by('-created_at')
    return render(request, 'Citizen/my_complaints.html', {'complaints': complaints})

@login_required
def citizen_complaint_details(request, id):
    if request.user.role != 'citizen':
        return redirect('dashboard')
    complaint = get_object_or_404(Complaint, id=id, citizen=request.user)
    return render(request, 'Citizen/complaint_detail.html', {'complaint': complaint})

@login_required
def citizen_feedback(request):
    if request.user.role != 'citizen':
        return redirect('dashboard')
    return render(request, 'Citizen/feedback.html')

@login_required
def citizen_notifications(request):
    if request.user.role != 'citizen':
        return redirect('dashboard')
    return render(request, 'Citizen/notification.html')

@login_required
def citizen_profile(request):
    if request.user.role != 'citizen':
        return redirect('dashboard')
    return render(request, 'Citizen/profile.html')

# Officer Views
@login_required
def officer_dashboard(request):
    if request.user.role != 'officer':
        return redirect('dashboard')
    
    # Fetch complaints assigned to this officer (or their department for now if direct assignment isn't used)
    # Assuming officers see all complaints in their department for this MVP, or specifically assigned ones.
    # Let's go with Department based for broader visibility as per "Command Center" feel.
    if request.user.department:
        complaints = Complaint.objects.filter(department=request.user.department)
    else:
        complaints = Complaint.objects.none()

    # Stats
    assigned_cases = complaints.count()
    pending_action = complaints.exclude(status__in=['resolved', 'rejected', 'closed']).count()
    
    from django.utils import timezone
    current_month = timezone.now().month
    resolved_month = complaints.filter(status='resolved', resolved_at__month=current_month).count()
    
    # Recent Assignments
    recent_assignments = complaints.order_by('-created_at')[:5]
    
    # AI Insights (Get the most recent high priority case)
    critical_case = complaints.filter(ai_predicted_priority='critical').exclude(status='resolved').first()
    
    context = {
        'assigned_cases': assigned_cases,
        'pending_action': pending_action,
        'resolved_month': resolved_month,
        'recent_assignments': recent_assignments,
        'critical_case': critical_case
    }
    
    return render(request, 'Officer_pages/1officer_dashboard.html', context)

# Dept Admin Views
@login_required
@login_required
def dept_dashboard(request):
    if request.user.role != 'dept_admin':
        return redirect('dashboard')
    
    # Fetch complaints for this department
    if request.user.department:
        complaints = Complaint.objects.filter(department=request.user.department)
    else:
        complaints = Complaint.objects.none()
        
    # Stats
    total_grievances = complaints.count()
    pending_review = complaints.filter(workflow_state='local_verified').count() # Verified by officer, pending dept review
    
    from django.utils import timezone
    current_day = timezone.now().day
    resolved_today = complaints.filter(status='resolved', resolved_at__day=current_day).count()
    escalated = complaints.filter(workflow_state__in=['city_pending', 'state_pending', 'national_pending']).count()
    
    # Monitoring Lists
    verified_complaints = complaints.filter(workflow_state='local_verified').order_by('-updated_at')[:5]
    rejected_complaints = complaints.filter(status='rejected').order_by('-updated_at')[:5]
    
    # --- Dynamic AI Insights ---
    from django.db.models import Count
    from django.utils import timezone
    import datetime
    
    # 1. Emerging Trend (Last 24 Hours)
    last_24h = timezone.now() - datetime.timedelta(hours=24)
    recent_complaints_24h = complaints.filter(created_at__gte=last_24h)
    
    emerging_trend = None
    trend_count = 0
    trend_location = "General"
    
    if recent_complaints_24h.exists():
        # Find most common category
        top_category = recent_complaints_24h.values('category__name').annotate(count=Count('id')).order_by('-count').first()
        if top_category:
            emerging_trend = top_category['category__name']
            trend_count = top_category['count']
            
            # Find most common location for this trend
            trend_complaints = recent_complaints_24h.filter(category__name=emerging_trend)
            # Simple location extraction (assuming location field exists or we use address)
            # For MVP, let's just say "Zone 1" or extract from description if location is not structured
            # We'll use a placeholder logic or if 'location' field exists
            trend_location = "Zone 4" # Placeholder or implement location grouping if model supports it
            
            # Calculate percentage increase (mock logic for MVP as we don't have historical baseline easily here)
            trend_percentage = 40 # Placeholder
    
    # 2. Routing Efficiency
    # Calculate % of complaints where ai_predicted_category matches the actual category (or department)
    # For now, since we auto-assign, it's high. Let's use average confidence score as a proxy for "Efficiency/Accuracy"
    from django.db.models import Avg
    avg_confidence = complaints.aggregate(Avg('ai_confidence_score'))['ai_confidence_score__avg'] or 0
    routing_efficiency = round(avg_confidence, 1)

    context = {
        'total_grievances': total_grievances,
        'pending_review': pending_review,
        'resolved_today': resolved_today,
        'escalated': escalated,
        'verified_complaints': verified_complaints,
        'rejected_complaints': rejected_complaints,
        'emerging_trend': emerging_trend,
        'trend_count': trend_count,
        'trend_location': trend_location,
        'trend_percentage': 40, # Static for now
        'routing_efficiency': routing_efficiency,
    }
    
    return render(request, 'Department_admin_pages.html/1Department_dashboard.html', context)

# State Admin Views
@login_required
def state_dashboard(request):
    if request.user.role != 'city_admin':
        return redirect('dashboard')
    return render(request, 'StateAdminPages/state_dashboard.html')

# National Admin Views
@login_required
def national_dashboard(request):
    if request.user.role != 'super_admin':
        return redirect('dashboard')
    
    # Global Stats
    total_complaints = Complaint.objects.count()
    total_users = User.objects.count()
    total_depts = Department.objects.count()
    
    # Recent Activity
    recent_complaints = Complaint.objects.order_by('-created_at')[:10]
    
    context = {
        'total_complaints': total_complaints,
        'total_users': total_users,
        'total_depts': total_depts,
        'recent_complaints': recent_complaints,
    }
    return render(request, 'NationalAdminPages/national_dashboard.html', context)

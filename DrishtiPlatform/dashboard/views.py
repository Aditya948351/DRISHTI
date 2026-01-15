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
    # Allow any authenticated user to view details if they have access (Role checks can be refined)
    # For now, allow all roles to view details to enable workflow
    complaint = get_object_or_404(Complaint, id=id)
    return render(request, 'complaints/complaint_detail.html', {'complaint': complaint})

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
        
    from accounts.forms import CitizenProfileForm
    
    # Check if profile is complete (using aadhaar as proxy)
    is_complete = bool(request.user.aadhaar_number)
    
    if not is_complete:
        if request.method == 'POST':
            form = CitizenProfileForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                # Check if profile was incomplete before this update
                was_incomplete = not request.user.aadhaar_number
                
                user = form.save(commit=False)
                
                # Award points if it was incomplete and now has aadhaar (meaning it's being completed)
                if was_incomplete and user.aadhaar_number:
                     user.points += 50
                
                user.save()
                return redirect('citizen_profile')
        else:
            form = CitizenProfileForm(instance=request.user)
        
        return render(request, 'Citizen/profile.html', {
            'is_complete': False,
            'form': form
        })

    # Mock Rewards Data
    rewards = [
        {'title': 'Municipal Tax Rebate', 'description': 'Get 5% off on property tax', 'points': 500, 'icon': 'percent', 'color': 'success'},
        {'title': 'Free Bus Pass', 'description': 'Monthly pass for city buses', 'points': 300, 'icon': 'bus', 'color': 'primary'},
        {'title': 'Public Library Membership', 'description': '1-year free membership', 'points': 200, 'icon': 'book-open', 'color': 'info'},
        {'title': 'Municipal Gym Access', 'description': '1-month free gym access', 'points': 150, 'icon': 'dumbbell', 'color': 'warning'},
        {'title': 'Tree Plantation Certificate', 'description': 'Plant a tree in your name', 'points': 100, 'icon': 'leaf', 'color': 'success'},
    ]
    
    return render(request, 'Citizen/profile.html', {'rewards': rewards, 'is_complete': True})

@login_required
def view_citizen_profile(request, user_id):
    # Only officers and admins can view
    if request.user.role not in ['officer', 'dept_admin', 'city_admin', 'super_admin']:
        return redirect('dashboard')
        
    from accounts.models import User
    target_user = get_object_or_404(User, id=user_id)
    
    # Ensure we are viewing a citizen
    if target_user.role != 'citizen':
        return redirect('dashboard') # Or show error
        
    return render(request, 'Citizen/view_profile.html', {'target_user': target_user})

from django.views.decorators.cache import never_cache

# Officer Views
@login_required
@never_cache
def officer_dashboard(request):
    if request.user.role != 'officer':
        print(f"DEBUG: User {request.user.username} is not an officer (Role: {request.user.role}). Redirecting.")
        return redirect('dashboard')
    
    print(f"DEBUG: officer_dashboard view called for user {request.user.username}")
    
    # Fetch complaints assigned to this officer (or their department for now if direct assignment isn't used)
    # Allow General Administration (Diksha) to see ALL complaints for triage
    if request.user.department and request.user.department.name != 'General Administration':
        complaints = Complaint.objects.filter(department=request.user.department)
    else:
        complaints = Complaint.objects.all()

    # Sort by Priority (Critical > High > Medium > Low)
    from django.db.models import Case, When, Value, IntegerField
    complaints = complaints.annotate(
        priority_val=Case(
            When(priority='critical', then=Value(1)),
            When(priority='high', then=Value(2)),
            When(priority='medium', then=Value(3)),
            When(priority='low', then=Value(4)),
            default=Value(5),
            output_field=IntegerField(),
        )
    ).order_by('priority_val', '-created_at')

    # Stats
    assigned_cases = complaints.count()
    pending_action = complaints.exclude(status__in=['resolved', 'rejected', 'closed']).count()
    
    from django.utils import timezone
    current_month = timezone.now().month
    resolved_month = complaints.filter(status='resolved', resolved_at__month=current_month).count()
    
    # Recent Assignments (Now sorted by priority)
    recent_assignments = complaints[:10]
    
    # AI Insights (Get the most recent high priority case)
    critical_case = complaints.filter(ai_predicted_priority='critical').exclude(status='resolved').first()
    
    context = {
        'assigned_cases': assigned_cases,
        'pending_action': pending_action,
        'resolved_month': resolved_month,
        'recent_assignments': recent_assignments,
        'critical_case': critical_case
    }
    
    # Use the consolidated V2 template
    return render(request, 'Officer_pages/1officer_dashboard_v2.html', context)

# Dept Admin Views
@login_required
@login_required
def dept_dashboard(request):
    if request.user.role != 'dept_admin':
        return redirect('dashboard')
    
    # Fetch complaints for this department
    # Fetch complaints for this department
    if request.user.department:
        if request.user.department.name == 'General Administration':
            complaints = Complaint.objects.all()
        else:
            complaints = Complaint.objects.filter(department=request.user.department)
    else:
        complaints = Complaint.objects.none()
        
    # Stats
    total_grievances = complaints.count()
    pending_review = complaints.filter(workflow_state='verified_by_officer').count() # Verified by officer, pending dept review
    
    from django.utils import timezone
    current_day = timezone.now().day
    resolved_today = complaints.filter(status='resolved', resolved_at__day=current_day).count()
    escalated = complaints.filter(workflow_state__in=['city_pending', 'state_pending', 'national_pending']).count()
    
    # Monitoring Lists
    # Monitoring Lists
    # For General Admin, show all relevant complaints. For others, filter by dept.
    if request.user.department and request.user.department.name == 'General Administration':
        verified_complaints = Complaint.objects.filter(workflow_state='verified_by_officer').order_by('-updated_at')[:5]
        rejected_complaints = Complaint.objects.filter(status='rejected').order_by('-updated_at')[:5]
        # Also show pending review complaints if any
        if not verified_complaints and not rejected_complaints:
             verified_complaints = Complaint.objects.all().order_by('-created_at')[:5]
    else:
        verified_complaints = complaints.filter(workflow_state='verified_by_officer').order_by('-updated_at')[:5]
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
@login_required
def state_dashboard(request):
    if request.user.role != 'city_admin' and request.user.role != 'state_admin': # Allow state_admin role if distinct
        # Fallback for now as we used 'city_admin' for state in some places, but created 'state_admin' users
        if request.user.role != 'state_admin' and request.user.role != 'city_admin':
             return redirect('dashboard')
    
    # Filter complaints (For now, all complaints as it's a state view)
    # In a real app, filter by State if address field was structured
    complaints = Complaint.objects.all()
    
    # 1. Key Stats
    total_grievances = complaints.count()
    resolved_count = complaints.filter(status='resolved').count()
    resolution_rate = int((resolved_count / total_grievances * 100)) if total_grievances > 0 else 0
    
    # Avg Days to Resolve
    from django.db.models import Avg, F, ExpressionWrapper, fields
    import datetime
    
    # Calculate duration for resolved complaints
    # SQLite might not support simple date diffs easily in Django ORM without specific functions
    # We will do a simple python calc for MVP if dataset is small, or use a simplified approach
    resolved_complaints = complaints.filter(status='resolved', resolved_at__isnull=False)
    total_days = 0
    count = 0
    for c in resolved_complaints:
        diff = c.resolved_at - c.created_at
        total_days += diff.days
        count += 1
    avg_days_resolve = round(total_days / count, 1) if count > 0 else 0
    
    critical_hotspots = complaints.filter(ai_predicted_priority='critical').count()
    
    # 2. Department Performance (Mapping to "Districts" table in template)
    from django.db.models import Count, Q
    dept_performance = Department.objects.annotate(
        total=Count('complaint'),
        resolved=Count('complaint', filter=Q(complaint__status='resolved')),
        pending=Count('complaint', filter=~Q(complaint__status='resolved'))
    )
    
    # Calculate a mock "AI Score" based on resolution rate
    for dept in dept_performance:
        if dept.total > 0:
            rate = (dept.resolved / dept.total) * 10
            dept.ai_score = round(rate, 1)
        else:
            dept.ai_score = 0

    context = {
        'total_grievances': total_grievances,
        'resolution_rate': resolution_rate,
        'avg_days_resolve': avg_days_resolve,
        'critical_hotspots': critical_hotspots,
        'dept_performance': dept_performance,
        'forwarded_complaints': complaints.filter(workflow_state='forwarded_to_redressal').order_by('-updated_at'),
    }
    return render(request, 'StateAdminPages/state_dashboard.html', context)

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

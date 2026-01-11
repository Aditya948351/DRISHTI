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
            status='pending'
        )
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
    return render(request, 'Officer_pages/1officer_dashboard.html')

# Dept Admin Views
@login_required
def dept_dashboard(request):
    if request.user.role != 'dept_admin':
        return redirect('dashboard')
    return render(request, 'Department_admin_pages.html/1Department_dashboard.html')

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
    return render(request, 'NationalAdminPages/national_dashboard.html')

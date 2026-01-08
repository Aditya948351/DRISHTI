from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from complaints.models import Complaint, Department

@login_required
def dashboard(request):
    user = request.user
    if user.role == 'citizen':
        return redirect('complaint_list')
    
    elif user.role == 'officer':
        assigned_complaints = Complaint.objects.filter(assigned_officer=user).exclude(status__in=['resolved', 'closed', 'rejected'])
        return render(request, 'dashboard/officer_dashboard.html', {'assigned_complaints': assigned_complaints})
    
    elif user.role == 'dept_admin':
        # Assuming dept admin belongs to a department
        if user.department:
            complaints = Complaint.objects.filter(department=user.department)
            stats = {
                'total': complaints.count(),
                'pending': complaints.exclude(status__in=['resolved', 'closed', 'rejected']).count(),
                'resolved': complaints.filter(status='resolved').count(),
            }
            recent_complaints = complaints.order_by('-created_at')[:10]
            return render(request, 'dashboard/dept_dashboard.html', {'stats': stats, 'recent_complaints': recent_complaints})
        else:
            return render(request, 'dashboard/dept_dashboard.html', {'error': 'No department assigned'})
            
    elif user.role == 'city_admin':
        # Aggregate stats
        return render(request, 'dashboard/city_dashboard.html')
        
    elif user.role == 'super_admin':
        return redirect('/admin/')
    else:
        return redirect('home')

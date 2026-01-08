from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Complaint
from .forms import ComplaintForm

from ai_engine.utils import predict_category, predict_priority, suggest_department
from .models import Category, Department

@login_required
def file_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.citizen = request.user
            
            # AI Triage
            pred_cat, cat_conf = predict_category(complaint.description)
            pred_prio, prio_conf = predict_priority(complaint.description, pred_cat)
            
            complaint.ai_predicted_category = pred_cat
            complaint.ai_predicted_priority = pred_prio
            complaint.ai_confidence_score = (cat_conf + prio_conf) / 2
            
            # Auto-fill if not provided (or suggest - here we auto-fill for MVP)
            if not complaint.category:
                # Try to find existing category or create/get default
                # For MVP, we might skip linking actual Category object if it doesn't exist
                # But let's try to find it by name
                category_obj = Category.objects.filter(name__icontains=pred_cat).first()
                if category_obj:
                    complaint.category = category_obj
            
            if not complaint.priority or complaint.priority == 'medium': # Default
                complaint.priority = pred_prio
                
            # Routing
            if not complaint.department and complaint.category:
                complaint.department = complaint.category.department
            
            complaint.status = 'ai_suggested' 
            complaint.save()
            return redirect('complaint_detail', pk=complaint.pk)
    else:
        form = ComplaintForm()
    return render(request, 'complaints/file_complaint.html', {'form': form})

@login_required
def complaint_list(request):
    complaints = Complaint.objects.filter(citizen=request.user).order_by('-created_at')
    return render(request, 'complaints/complaint_list.html', {'complaints': complaints})

@login_required
def complaint_detail(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    # Ensure citizen can only see their own, or officers can see assigned/dept
    # For now, simple check
    if request.user.role == 'citizen' and complaint.citizen != request.user:
        return redirect('home') # Or 403
    
    return render(request, 'complaints/complaint_detail.html', {'complaint': complaint})

@login_required
def update_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    # Check permissions (officer or admin)
    if request.user.role not in ['officer', 'dept_admin', 'super_admin']:
        return redirect('home') # Or 403
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            complaint.status = new_status
            if new_status == 'resolved':
                from django.utils import timezone
                complaint.resolved_at = timezone.now()
            complaint.save()
            # Log activity (TODO)
            return redirect('complaint_detail', pk=pk)
    
    return redirect('complaint_detail', pk=pk)

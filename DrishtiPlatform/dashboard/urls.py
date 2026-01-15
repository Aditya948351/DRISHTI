from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Shared System Pages
    path('shared/error/', views.shared_error, name='shared_error'),
    path('shared/redirect/', views.shared_redirect, name='shared_redirect'),
    
    # Citizen
    path('citizen/dashboard/', views.citizen_dashboard, name='citizen_dashboard'),
    path('citizen/submit-complaint/', views.citizen_submit_complaint, name='citizen_submit_complaint'),
    path('citizen/my-complaints/', views.citizen_my_complaints, name='citizen_my_complaints'),
    path('citizen/complaint-details/<int:id>/', views.citizen_complaint_details, name='citizen_complaint_details'),
    path('citizen/feedback/', views.citizen_feedback, name='citizen_feedback'),
    path('citizen/notifications/', views.citizen_notifications, name='citizen_notifications'),
    path('citizen/profile/', views.user_profile, name='citizen_profile'),
    
    # Officer
    path('officer/dashboard/', views.officer_dashboard, name='officer_dashboard'),
    path('officer/profile/', views.user_profile, name='officer_profile'),
    
    # Dept Admin
    path('dept/dashboard/', views.dept_dashboard, name='dept_dashboard'),
    
    # State Admin
    path('state/dashboard/', views.state_dashboard, name='state_dashboard'),
    
    # National Admin
    path('national/dashboard/', views.national_dashboard, name='national_dashboard'),
    
    # Analytics
    path('analytics/dashboard/', views.analytics_dashboard, name='analytics_dashboard'),
]

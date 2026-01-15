"""
URL configuration for DrishtiPlatform project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from complaints import views as complaints_views
from dashboard import views as dashboard_views

urlpatterns = [
    # --- Public Pages ---
    path('', TemplateView.as_view(template_name='PublicPages/home.html'), name='root'),
    path('home/', TemplateView.as_view(template_name='PublicPages/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='PublicPages/about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='PublicPages/contact.html'), name='contact'),
    path('faq/', TemplateView.as_view(template_name='PublicPages/faq.html'), name='faq'),
    path('complaint/track/', complaints_views.track_complaint_status, name='track_complaint'),

    # --- Authentication ---
    path('login/', accounts_views.CustomLoginView.as_view(), name='login'),
    path('register/', accounts_views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password/reset/', TemplateView.as_view(template_name='PublicPages/reset_password.html'), name='reset_password'),

    # --- Citizen Portal ---
    path('dashboard/', dashboard_views.dashboard, name='dashboard'),
    path('citizen/dashboard/', dashboard_views.citizen_dashboard, name='citizen_dashboard'),
    path('citizen/complaints/new/', complaints_views.file_complaint, name='file_complaint'),
    path('citizen/complaints/', complaints_views.complaint_list, name='citizen_complaints'),
    path('citizen/complaints/<int:pk>/', complaints_views.complaint_detail, name='complaint_detail'),
    path('citizen/complaints/<int:pk>/feedback/', dashboard_views.citizen_feedback, name='complaint_feedback'),
    path('citizen/profile/', dashboard_views.user_profile, name='citizen_profile'),
    path('citizen/profile/<int:user_id>/', dashboard_views.view_citizen_profile, name='view_citizen_profile'),
    path('citizen/notifications/', dashboard_views.citizen_notifications, name='citizen_notifications'),
    
    # Community & Assistant
    path('citizen/community/', include('community.urls')),
    path('citizen/assistant/', TemplateView.as_view(template_name='ai_engine/assistant.html'), name='ai_assistant'),

    # --- Officer Portal ---
    path('officer/dashboard/', dashboard_views.officer_dashboard, name='officer_dashboard'),
    path('officer/complaints/assigned/', complaints_views.complaint_list, {'filter': 'assigned'}, name='officer_assigned_complaints'),
    path('officer/complaints/<int:pk>/work/', complaints_views.update_status, name='officer_work_complaint'),
    path('officer/ai/inbox/', TemplateView.as_view(template_name='ai_engine/inbox.html'), name='officer_ai_inbox'),
    path('officer/analytics/', dashboard_views.analytics_dashboard, name='analytics_dashboard'),

    # --- Department Admin ---
    path('dept/dashboard/', dashboard_views.dept_dashboard, name='dept_dashboard'),
    path('dept/reports/', TemplateView.as_view(template_name='dashboard/reports.html'), name='dept_reports'),

    # --- State/System Admin ---
    path('state/dashboard/', dashboard_views.state_dashboard, name='state_dashboard'),
    path('admin/system/dashboard/', dashboard_views.national_dashboard, name='national_dashboard'),
    
    # --- Django Admin ---
    path('admin/', admin.site.urls),
    
    # --- Shared/Errors ---
    path('health/', TemplateView.as_view(template_name='health.html'), name='health'),
    path('health/', TemplateView.as_view(template_name='health.html'), name='health'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

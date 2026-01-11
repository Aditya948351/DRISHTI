"""
URL configuration for DrishtiPlatform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Public Pages
    path('home/', TemplateView.as_view(template_name='PublicPages/home.html'), name='home'),
    path('', TemplateView.as_view(template_name='PublicPages/home.html'), name='root'),
    path('about/', TemplateView.as_view(template_name='PublicPages/about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='PublicPages/contact.html'), name='contact'),
    path('track-complaint/', TemplateView.as_view(template_name='PublicPages/track_complaint.html'), name='track_complaint'),
    path('faq/', TemplateView.as_view(template_name='PublicPages/faq.html'), name='faq'),

    # Auth
    path('login/', accounts_views.CustomLoginView.as_view(), name='login'),
    path('register/', accounts_views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset-password/', TemplateView.as_view(template_name='PublicPages/reset_password.html'), name='reset_password'),

    # Existing Includes
    path('accounts/', include('accounts.urls')),
    path('complaints/', include('complaints.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('community/', include('community.urls')),
]

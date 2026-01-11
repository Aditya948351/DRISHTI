from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='accounts_register'),
    path('login/', views.CustomLoginView.as_view(), name='accounts_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='accounts_logout'),
]

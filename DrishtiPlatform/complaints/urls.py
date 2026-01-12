from django.urls import path
from . import views

urlpatterns = [
    path('file/', views.file_complaint, name='file_complaint'),
    path('my-complaints/', views.complaint_list, name='citizen_complaints'),
    path('<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('<int:pk>/update-status/', views.update_status, name='update_status'),
]

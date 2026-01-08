from django.urls import path
from . import views

urlpatterns = [
    path('', views.thread_list, name='thread_list'),
    path('create/', views.create_thread, name='create_thread'),
    path('<int:pk>/', views.thread_detail, name='thread_detail'),
]

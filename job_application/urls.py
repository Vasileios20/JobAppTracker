from django.urls import path
from . import views

urlpatterns = [
    path('job/', views.job_application, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

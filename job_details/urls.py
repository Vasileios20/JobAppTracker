from django.urls import path
from . import views

app_name = 'job_details'

urlpatterns = [
    path('job/<int:pk>/', views.job_detail, name='job_detail'),
    path('job/<int:pk>/edit/', views.JobEditView.as_view(), name='edit_job'),
    path('job/<int:pk>/delete/', views.JobDeleteView.as_view(), name='delete_job'),
]
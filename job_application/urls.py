from django.urls import path
from . import views
from .views import JobFormView

urlpatterns = [
    path('', views.job_application, name='job_application'),
    path('job-form', JobFormView.as_view(), name='job_form'),
    path('filter/', views.filter_jobs, name='filter'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('api/get-job-titles/', views.get_job_titles, name='get_job_titles'),
]

from django.urls import path
from . import views
from .views import JobApplicationView

urlpatterns = [
    path('', views.job_application, name='job_application'),
    path('job-form', JobApplicationView.as_view(), name='job_form'),

    path('filter/', views.filter_jobs, name='filter'),
    path('statistics/', views.statistics_view, name='statistics'),

]

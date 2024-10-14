from django.urls import path
from . import views

urlpatterns = [

    path('job/', views.job_application, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('', views.job_application, name='job_application'),
    path('filter/', views.filter_jobs, name='filter'),
    path('statistics/', views.statistics_view, name='statistics'),

]

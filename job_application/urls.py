from django.urls import path
from . import views
from .views import JobFormView

urlpatterns = [
    path('', views.job_application, name='job_application'),
    path('job-form', JobFormView.as_view(), name='job_form'),
    path('filter/', views.filter_jobs, name='filter'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('api/get-job-titles/', views.get_job_titles, name='get_job_titles'),
    path('job/<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('job/<int:job_id>/delete/', views.delete_job_view, name='delete_job'),
    path('job/<int:job_id>/add_note/', views.add_note_view, name='add_note'),
    path('note/<int:note_id>/update/',
         views.update_note_view, name='update_note'),
    path('note/<int:note_id>/delete/',
         views.delete_note_view, name='delete_note'),
]

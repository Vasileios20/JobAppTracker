from django.shortcuts import render
from .models import JobApplication
from django.conf import settings


def job_application(request):
    return render(request, 'job_app.html')


def dashboard(request):
    applications = JobApplication.objects.all()
    context = {
        'applications': applications,
        'adzuna_app_id': settings.ADZUNA_APP_ID,
        'adzuna_api_key': settings.ADZUNA_API_KEY
    }
    return render(request, 'dashboard.html', context)

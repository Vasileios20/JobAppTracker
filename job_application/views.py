import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q, Count
from django.utils import timezone
from .models import Job
from django.views import View
# from .adzuna_integration import get_job_titles
import os

ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID')
ADZUNA_APP_KEY = os.getenv('ADZUNA_API_KEY')
BASE_URL = 'https://api.adzuna.com/v1/api/jobs/us/search/1'


def job_application(request):
    applications = Job.objects.all()
    context = {
        'applications': applications,
        'adzuna_app_id': settings.ADZUNA_APP_ID,
        'adzuna_api_key': settings.ADZUNA_API_KEY
    }
    return render(request, 'job_app.html', context)


class JobApplicationView(View):
    def get(self, request):

        # Fetch data from Adzuna API
        job_data = self.fetch_job_data()

        categories = ["Software Development", "Data Science",
                      "Marketing", "Sales"]  # Example categories

        # Render the form with fetched job data
        return render(request, 'job_form.html', {
            'categories': categories,  # Pass predefined categories
            'job_data': job_data,  # Pass the job titles and company names
        })

    def fetch_job_data(self, ):

        # Prepare the API request URL for Adzuna
        url = (
            f"https://api.adzuna.com/v1/api/jobs/us/search/1"
            f"?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_APP_KEY}"
            f"&results_per_page=10&what=developer"
        )

        response = requests.get(url)
        if response.status_code == 200:
            job_data = response.json().get('results', [])
            return job_data
        return []

    def save_application(request):
        if request.method == 'POST':
            job_title = request.POST.get('title')
            status = request.POST.get('status')
            company = request.POST.get('company')
            location = request.POST.get('location')
            category = request.POST.get('category')
            date_applied = request.POST.get('date-applied')

            # Save the job application logic
            job = Job(
                title=job_title,
                status=status,
                company=company,
                location=location,
                category=category,
                date_applied=date_applied,
                user=request.user
            )
            job.save()

            return redirect('job_dashboard')


# def dashboard(request):
#     # Use Job model instead of JobApplication
#     applications = Job.objects.all()
#     context = {
#         'applications': applications,
#         'adzuna_app_id': settings.ADZUNA_APP_ID,
#         'adzuna_api_key': settings.ADZUNA_API_KEY
#     }
#     return render(request, 'job_ap.html', context)


def filter_jobs(request):
    query = request.GET.get('query')
    if query:
        jobs = Job.objects.filter(
            Q(company__icontains=query) | Q(title__icontains=query) |
            Q(category__icontains=query) | Q(location__icontains=query) |
            Q(status__icontains=query)
        )
    else:
        jobs = Job.objects.all()

    return render(request, 'job_list.html', {'jobs': jobs})


def statistics_view(request):
    all_applications = Job.objects.filter(user=request.user)

    total_applications = all_applications.count()

    status_counts = all_applications.values(
        'status').annotate(count=Count('status'))

    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    trend_data = all_applications.filter(date_applied__gte=thirty_days_ago) \
        .values('date_applied') \
        .annotate(count=Count('id')) \
        .order_by('date_applied')

    top_companies = all_applications.values('company') \
        .annotate(count=Count('company')) \
        .order_by('-count')[:5]

    success_count = all_applications.filter(status='Offer').count()
    success_rate = round((success_count / total_applications)
                         * 100, 2) if total_applications > 0 else 0

    context = {
        'total_applications': total_applications,
        'status_counts': status_counts,
        'trend_data': trend_data,
        'top_companies': top_companies,
        'success_rate': success_rate
    }

    return render(request, 'statistics.html', context)

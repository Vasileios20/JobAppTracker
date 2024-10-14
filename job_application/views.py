import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.db.models import Q, Count
from django.utils import timezone
from .models import Job
from django.views import View
from django.http import JsonResponse
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


class JobFormView(View):
    def get(self, request):
        # Fetch categories from Adzuna API
        categories = self.fetch_categories()

        # Fetch job titles for the first category (default)
        if categories:
            # Use the first category as default
            selected_category = categories[0]['tag']
            job_data = self.fetch_job_titles(selected_category)
        else:
            selected_category = None
            job_data = []

        return render(request, 'job_form.html', {
            'categories': categories,
            'job_data': job_data,
            'selected_category': selected_category,
        })

    def post(self, request):
        # Save the job application
        job_title = request.POST.get('title')
        company_name = request.POST.get('company')
        category = request.POST.get('category')
        date_applied = request.POST.get('date_applied')
        status = request.POST.get('status')

        # Save the job in the database
        Job.objects.create(
            title=job_title,
            company=company_name,
            category=category,
            date_applied=date_applied,
            status=status,
            user=request.user
        )
        return redirect('job_application')

    def fetch_categories(self):
        # Fetch job categories from Adzuna API
        url = f"http://api.adzuna.com/v1/api/jobs/gb/categories?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_APP_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            categories_data = response.json().get('results', [])
            # Each category has 'tag' (for API queries) and 'label' (for display)
            categories = [{'tag': category['tag'], 'label': category['label']}
                          for category in categories_data]
            return categories
        return []

    def fetch_job_titles(self, category):
        # Fetch job titles for a selected category from Adzuna API
        url = (
            f"https://api.adzuna.com/v1/api/jobs/gb/search/1"
            f"?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_APP_KEY}"
            f"&category={category}&results_per_page=10"
        )
        response = requests.get(url)
        if response.status_code == 200:
            job_data = response.json().get('results', [])
            return job_data
        return []


def get_job_titles(request):
    category = request.GET.get('category')
    if category:
        job_data = JobFormView().fetch_job_titles(category)
        return JsonResponse(job_data, safe=False)
    return JsonResponse([], safe=False)


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

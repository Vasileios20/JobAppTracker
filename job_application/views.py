import requests
from django.shortcuts import render
from django.conf import settings
from django.db.models import Q, Count
from django.utils import timezone
from .models import Job

# Function to get categories from Adzuna API
def get_adzuna_categories():
    url = f"https://api.adzuna.com/v1/api/jobs/us/categories?app_id={settings.ADZUNA_APP_ID}&app_key={settings.ADZUNA_API_KEY}&what=software"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [category['tag'] for category in data['results']]
    else:
        # Log or print an error message in case the request fails
        print(f"Failed to fetch categories: {response.status_code}")
        return []

# Function to get software job titles and companies from Adzuna API
def get_adzuna_job_data():
    url = f"https://api.adzuna.com/v1/api/jobs/us/search/1?app_id={settings.ADZUNA_APP_ID}&app_key={settings.ADZUNA_API_KEY}&what=software"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        job_data = [(job['title'], job['company']['display_name']) for job in data['results']]
        return job_data
    else:
        # Log or print an error message in case the request fails
        print(f"Failed to fetch job data: {response.status_code}")
        return []

# View to render job application form with categories and software job data from Adzuna API
def job_application(request):
    categories = get_adzuna_categories()
    job_data = get_adzuna_job_data()

    context = {
        'categories': categories,
        'job_data': job_data,
        'applications': Job.objects.all()
    }

    return render(request, 'job_app.html', context)

# View for the job application dashboard
def dashboard(request):
    # Use Job model instead of JobApplication
    applications = Job.objects.all()
    context = {
        'applications': applications,
        'adzuna_app_id': settings.ADZUNA_APP_ID,
        'adzuna_api_key': settings.ADZUNA_API_KEY
    }
    return render(request, 'dashboard.html', context)

# View to filter job listings based on a query
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

# View to display job application statistics
def statistics_view(request):
    all_applications = Job.objects.filter(user=request.user)
    
    total_applications = all_applications.count()
    
    status_counts = all_applications.values('status').annotate(count=Count('status'))
    
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    trend_data = all_applications.filter(date_applied__gte=thirty_days_ago) \
        .values('date_applied') \
        .annotate(count=Count('id')) \
        .order_by('date_applied')
    
    top_companies = all_applications.values('company') \
        .annotate(count=Count('company')) \
        .order_by('-count')[:5]
    
    success_count = all_applications.filter(status='Offer').count()
    success_rate = round((success_count / total_applications) * 100, 2) if total_applications > 0 else 0
    
    context = {
        'total_applications': total_applications,
        'status_counts': status_counts,
        'trend_data': trend_data,
        'top_companies': top_companies,
        'success_rate': success_rate
    }
    
    return render(request, 'statistics.html', context)


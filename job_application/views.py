from django.shortcuts import render
from django.db.models import Q, Count
from django.utils import timezone
from .models import Job

def job_application(request):
    return render(request, 'job_app.html')

def filter_jobs(request):
    query = request.GET.get('query')
    if query:
        jobs = Job.objects.filter(
            Q(company__icontains=query) | Q(title__icontains=query) | Q(
                category__icontains=query) | Q(location__icontains=query) |
            Q(status__icontains=query)
        )
    else:
        jobs = Job.objects.all()

    return render(request, 'job_list.html', {'jobs': jobs})

def statistics_view(request):
    # Get all job applications (assuming we're not filtering by user for now)
    all_applications = Job.objects.all()

    # Calculate total applications
    total_applications = all_applications.count()

    # Calculate applications by status
    status_counts = all_applications.values('status').annotate(count=Count('status'))

    # Calculate application trend over time (last 30 days)
    thirty_days_ago = timezone.now().date() - timezone.timedelta(days=30)
    trend_data = all_applications.filter(date_applied__gte=thirty_days_ago) \
        .values('date_applied') \
        .annotate(count=Count('id')) \
        .order_by('date_applied')

    context = {
        'total_applications': total_applications,
        'status_counts': status_counts,
        'trend_data': trend_data,
    }

    return render(request, 'statistics.html', context)
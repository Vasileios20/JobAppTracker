from django.shortcuts import render
from django.db.models import Q, Count
from django.utils import timezone
from .models import Job
import datetime


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

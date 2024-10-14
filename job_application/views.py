from django.shortcuts import render
from django.conf import settings
from django.db.models import Q, Count
from django.utils import timezone
from .models import Job
import datetime
from django.db.models.functions import TruncDate
from datetime import timedelta


def job_application(request):
    return render(request, 'job_app.html')

def dashboard(request):
    # Use Job model instead of JobApplication
    applications = Job.objects.all()
    context = {
        'applications': applications,
        'adzuna_app_id': settings.ADZUNA_APP_ID,
        'adzuna_api_key': settings.ADZUNA_API_KEY
    }
    return render(request, 'dashboard.html', context)


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
    # Get the date range from the request, default to 30 days
    days = int(request.GET.get('days', 30))
    if days == 0:  # 'all time'
        start_date = None
    else:
        start_date = timezone.now().date() - timezone.timedelta(days=days)

    all_applications = Job.objects.filter(user=request.user)
    if start_date:
        all_applications = all_applications.filter(date_applied__gte=start_date)

    total_applications = all_applications.count()
    
    # Success Rate
    success_count = all_applications.filter(status='Offer').count()
    success_rate = round((success_count / total_applications) * 100, 2) if total_applications > 0 else 0
    
    # Response Rate
    response_count = all_applications.exclude(status='Applied').count()
    response_rate = round((response_count / total_applications) * 100, 2) if total_applications > 0 else 0
    
    # Job Seeker Level
    experience_points = total_applications * 10 + success_count * 50
    job_seeker_level = experience_points // 100 + 1
    next_level_points = job_seeker_level * 100
    
    status_counts = all_applications.values('status').annotate(count=Count('status'))
    
    # Application Trend
    trend_data = all_applications.annotate(
        date=TruncDate('date_applied')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    # Ensure all dates in the range have a data point
    all_dates = {(start_date + timedelta(days=i)).isoformat(): 0 for i in range((timezone.now().date() - start_date).days + 1)}
    for item in trend_data:
        all_dates[item['date'].isoformat()] = item['count']
    trend_data = [{'date': date, 'count': count} for date, count in all_dates.items()]
    
    top_companies = all_applications.values('company').annotate(count=Count('company')).order_by('-count')[:5]
    
    # Streak calculation
    applications_by_date = all_applications.values('date_applied__date').annotate(count=Count('id')).order_by('date_applied__date')
    current_streak = 0
    longest_streak = 0
    streak = 0
    last_date = None
    for app in applications_by_date:
        if last_date and app['date_applied__date'] == last_date + timedelta(days=1):
            streak += 1
        else:
            streak = 1
        current_streak = streak if app['date_applied__date'] == timezone.now().date() else 0
        longest_streak = max(longest_streak, streak)
        last_date = app['date_applied__date']

    # Achievements (example)
    achievements = [
        {'name': 'First Application', 'points': 10},
        {'name': 'Interview Ace', 'points': 50},
        {'name': 'Offer Received', 'points': 100},
    ]
    
    context = {
        'total_applications': total_applications,
        'success_rate': success_rate,
        'response_rate': response_rate,
        'job_seeker_level': job_seeker_level,
        'experience_points': experience_points,
        'next_level_points': next_level_points,
        'status_counts': status_counts,
        'trend_data': trend_data,
        'top_companies': top_companies,
        'achievements': achievements,
        'current_streak': current_streak,
        'longest_streak': longest_streak,
    }
    
    return render(request, 'statistics.html', context)
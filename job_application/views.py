import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.db.models import Q, Count
from django.utils import timezone
from .models import Job, Note
from .forms import NoteForm
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import os

ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID')
ADZUNA_APP_KEY = os.getenv('ADZUNA_API_KEY')
BASE_URL = 'https://api.adzuna.com/v1/api/jobs/us/search/1'


@login_required
def job_application(request):
    user = request.user
    applications = Job.objects.all().filter(user=user)
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
        location = request.POST.get('location')
        date_applied = request.POST.get('date_applied')
        status = request.POST.get('status')

        # Save the job in the database
        Job.objects.create(
            title=job_title,
            company=company_name,
            category=category,
            location=location,
            date_applied=date_applied,
            status=status,
            user=request.user
        )
        return redirect('job_application')

    def fetch_categories(self):
        # Fetch job categories from Adzuna API
        url = (
            f"http://api.adzuna.com/v1/api/jobs/gb/categories"
            f"?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_APP_KEY}"
        )
        response = requests.get(
            url
        )
        if response.status_code == 200:
            categories_data = response.json().get('results', [])
            # Each category has 'tag' (for API queries) and 'label' for display
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


@login_required
def job_detail_view(request, job_id):
    # Fetch the specific job by its ID
    job = get_object_or_404(Job, id=job_id, user=request.user)
    notes = job.notes.all()

    # If the request method is POST, it means we are trying to update the job
    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.company = request.POST.get('company')
        job.category = request.POST.get('category')
        job.location = request.POST.get('location')
        job.date_applied = request.POST.get('date_applied')
        job.status = request.POST.get('status')
        job.save()  # Save the updated job to the database

        # Redirect back to the job list after saving
        return redirect('job_application')

    context = {
        'job': job,
        'notes': notes
    }

    # Render the job detail form with the existing job data
    return render(request, 'job_application/job_application.html', context)


@login_required
def delete_job_view(request, job_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)
    job.delete()
    return redirect(reverse('job_application'))


@login_required
def add_note_view(request, job_id):
    job = get_object_or_404(Job, id=job_id, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.job = job
            note.save()
            return redirect('job_detail', job_id=job.id)
    else:
        form = NoteForm()

    return render(request, 'add_note.html', {'form': form, 'job': job})


@login_required
def update_note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, job__user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('job_detail', job_id=note.job.id)
    else:
        form = NoteForm(instance=note)

    return render(request, 'update_note.html', {'form': form, 'note': note})


@login_required
def delete_note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id, job__user=request.user)
    note.delete()
    return redirect('job_detail', job_id=note.job.id)


@login_required
def get_job_titles(request):
    category = request.GET.get('category')
    if category:
        job_data = JobFormView().fetch_job_titles(category)
        return JsonResponse(job_data, safe=False)
    return JsonResponse([], safe=False)


@login_required
def filter_jobs(request):
    user = request.user
    query = request.GET.get('query')
    if query:
        applications = Job.objects.filter(
            Q(company__icontains=query) | Q(title__icontains=query) |
            Q(category__icontains=query) | Q(location__icontains=query) |
            Q(status__icontains=query),
            user=user
        )
    else:
        applications = Job.objects.filter(user=user)

    return render(request, 'job_app.html', {'applications': applications})


@login_required
def statistics_view(request):
    # Get the date range from the request, default to 30 days
    days = int(request.GET.get('days', 30))
    if days == 0:  # 'all time'
        start_date = None
    else:
        start_date = timezone.now().date() - timezone.timedelta(days=days)

    all_applications = Job.objects.filter(user=request.user)
    if start_date:
        all_applications = all_applications.filter(
            date_applied__gte=start_date)

    total_applications = all_applications.count()

    # Success Rate
    success_count = all_applications.filter(status='Offer').count()
    success_rate = round((success_count / total_applications)
                         * 100, 2) if total_applications > 0 else 0

    # Response Rate
    response_count = all_applications.exclude(status='Applied').count()
    response_rate = round((response_count / total_applications)
                          * 100, 2) if total_applications > 0 else 0

    # Job Seeker Level
    experience_points = total_applications * 10 + success_count * 50
    job_seeker_level = experience_points // 100 + 1
    next_level_points = job_seeker_level * 100

    status_counts = all_applications.values(
        'status').annotate(count=Count('status'))

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
    trend_data = [{'date': date, 'count': count}
                  for date, count in all_dates.items()]

    top_companies = all_applications.values('company').annotate(
        count=Count('company')).order_by('-count')[:5]

    # Streak calculation
    applications_by_date = all_applications.values('date_applied__date').annotate(
        count=Count('id')).order_by('date_applied__date')
    current_streak = 0
    longest_streak = 0
    streak = 0
    last_date = None
    for app in applications_by_date:
        if last_date and app['date_applied__date'] == last_date + timedelta(days=1):
            streak += 1
        else:
            streak = 1
        current_streak = streak if app['date_applied__date'] == timezone.now(
        ).date() else 0
        longest_streak = max(longest_streak, streak)
        last_date = app['date_applied__date']

    # Achievements (example)
    achievements = [
        {'name': 'First Application', 'points': 10},
        {'name': 'Interview Ace', 'points': 50},
        {'name': 'Offer Received', 'points': 100},
    ]

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

    # Enhanced Achievements
    all_achievements = [
        {'name': 'First Application', 'icon': 'paper-plane',
            'description': 'Submit your first job application', 'xp': 10, 'condition': total_applications >= 1},
        {'name': 'Persistent Applier', 'icon': 'calendar-check',
            'description': 'Apply to jobs for 7 days in a row', 'xp': 50, 'condition': longest_streak >= 7},
        {'name': 'Interview Ready', 'icon': 'user-tie', 'description': 'Get invited to 5 interviews',
            'xp': 30, 'condition': all_applications.filter(status='Interview').count() >= 5},
        {'name': 'Offer Received', 'icon': 'award', 'description': 'Receive your first job offer',
            'xp': 100, 'condition': success_count >= 1},
        {'name': 'Application Master', 'icon': 'star', 'description': 'Submit 50 job applications',
            'xp': 200, 'condition': total_applications >= 50},
    ]

    achievements = [
        {**achievement, 'unlocked': achievement['condition']}
        for achievement in all_achievements
    ]

    # Calculate total XP from achievements
    achievement_xp = sum(ach['xp'] for ach in achievements if ach['unlocked'])

    # Quests (example - you might want to store these in the database)
    active_quests = [
        {
            'name': 'Application Spree',
            'description': 'Apply to 10 jobs this week',
            'progress': min(all_applications.filter(date_applied__gte=timezone.now() - timedelta(days=7)).count() / 10 * 100, 100),
            'xp_reward': 50
        },
        {
            'name': 'Diverse Applications',
            'description': 'Apply to jobs at 5 different companies',
            'progress': min(all_applications.values('company').distinct().count() / 5 * 100, 100),
            'xp_reward': 30
        },
        {
            'name': 'Interview Prep',
            'description': 'Update your resume and complete 3 mock interviews',
            'progress': 60,  # This would typically be calculated based on user actions
            'xp_reward': 40
        },
    ]

    # Recalculate total XP including achievements and quest rewards
    total_xp = (
        total_applications * 10 +  # XP for applications
        success_count * 50 +       # XP for successful applications
        achievement_xp +           # XP from achievements
        # XP from completed quests
        sum(quest['xp_reward']
            for quest in active_quests if quest['progress'] == 100)
    )

    # Adjusted level calculation
    job_seeker_level = (total_xp // 100) + 1
    next_level_points = job_seeker_level * 100
    xp_to_next_level = next_level_points - total_xp

    # XP Gain Guide
    xp_gain_guide = [
        {'action': 'Apply to a job', 'xp': 10},
        {'action': 'Get an interview', 'xp': 20},
        {'action': 'Complete an interview', 'xp': 30},
        {'action': 'Receive a job offer', 'xp': 50},
        {'action': 'Update your resume', 'xp': 5},
        {'action': 'Complete a mock interview', 'xp': 15},
    ]

    # Funnel Data
    funnel_data = {
        'applied': total_applications,
        'reviewed': all_applications.exclude(status='Applied').count(),
        'interviewed': all_applications.filter(status__in=['Interview', 'Offer']).count(),
        'offered': success_count
    }

    # Skills Data (you may want to replace this with actual user skills data)
    skills_data = {
        'labels': ['Python', 'JavaScript', 'React', 'Django', 'SQL', 'Git'],
        'data': [85, 75, 70, 80, 65, 90]
    }

    # Job Search Timeline
    timeline_data = all_applications.order_by(
        'date_applied').values('date_applied', 'company', 'status')
    job_search_events = [
        {
            'date': item['date_applied'].strftime('%Y-%m-%d'),
            'type': item['status'],
            'description': f"Applied to {item['company']}"
        }
        for item in timeline_data
    ]

    # Job Locations (using only the 'location' field)
    job_locations = all_applications.values('company', 'location').distinct()

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
        'total_applications': total_applications,
        'success_rate': success_rate,
        'response_rate': response_rate,
        'job_seeker_level': job_seeker_level,
        'experience_points': total_xp,
        'next_level_points': next_level_points,
        'xp_to_next_level': xp_to_next_level,
        'status_counts': status_counts,
        'trend_data': trend_data,
        'top_companies': top_companies,
        'achievements': achievements,
        'current_streak': current_streak,
        'longest_streak': longest_streak,
        'active_quests': active_quests,
        'xp_gain_guide': xp_gain_guide,
        'status_counts': [{'status': item['status'], 'count': item['count']} for item in status_counts],
        'trend_data': [{'date': item['date_applied'].strftime('%Y-%m-%d'), 'count': item['count']} for item in trend_data],
        'funnelData': funnel_data,
        'skillsData': skills_data,
        'timelineData': job_search_events,
        'jobLocations': list(job_locations),
    }

    return render(request, 'statistics.html', context)

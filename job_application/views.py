from django.shortcuts import render
from django.db.models import Q
from .models import Job


def job_application(request):
    return render(request, 'job_app.html')


def filter_jobs(request):
    query = request.GET.get('query')
    print(query)
    if query:
        jobs = Job.objects.filter(
            Q(company_name__icontains=query) | Q(job_title__icontains=query)
        )
        print(jobs)
    else:
        jobs = Job.objects.all()
        print(jobs)

    return render(request, 'job_list.html', {'jobs': jobs})

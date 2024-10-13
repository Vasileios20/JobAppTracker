from django.shortcuts import render


def job_application(request):
    return render(request, 'job_app.html')

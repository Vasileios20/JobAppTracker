from django.shortcuts import render


# Create your views here.


def job_application(request):
    return render(request, 'job_app.html')


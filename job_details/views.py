from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView
from .models import Job

@login_required
def job_detail(request, pk):
    try:
        # Attempt to get the job by pk and user
        job = get_object_or_404(Job, pk=pk, user=request.user)
        return render(request, 'job_details/job_detail.html', {'job': job})
    except Exception as e:
        # Print error for debugging
        print(f"Error: {e}")
        return render(request, 'job_details/job_detail.html', {'error': 'Job not found.'})
# Edit Job
class JobEditView(UpdateView):
    model = Job
    fields = ['category', 'company', 'title', 'location', 'url', 'status']
    template_name = 'job_details/job_edit.html'

    def get_success_url(self):
        return reverse_lazy('job_details:job_detail', kwargs={'pk': self.object.pk})

# Delete Job
class JobDeleteView(DeleteView):
    model = Job
    template_name = 'job_details/job_confirm_delete.html'
    success_url = reverse_lazy('job_details:job_list')
from django.shortcuts import render, redirect, get_object_or_404 #render() combines a template with context data and returns an HTML response to the browser

from .models import JobApplication
from .forms import AddJobForm
from django.contrib import messages

def job_list(request): #request is a built-in object that represents the HTTP request sent by the browser
    status_filter=request.GET.get('status')
    sort_by=request.GET.get('sort', 'application_date')  #default sorting


    jobs=JobApplication.objects.all()

#If a specific status is selected (not "All"), the queryset is filtered to show only jobs with that status
    if status_filter and status_filter!='All':
        jobs=jobs.filter(status=status_filter)

#If the sorting choice is valid, it sorts the jobs accordingly
    if sort_by in['application_date', 'company_name']:
        jobs=jobs.order_by(sort_by)

    status_options=['All', 'Applied', 'Interview', 'Offer', 'Rejected']
        
#Renders the updated list to the job_list.html template, passing the filtered and sorted jobs list, and the selected values to prefill the form
    return render(request, 'tracker/job_list.html',{'jobs': jobs,
         'selected_status': status_filter or 'All',
         'selected_sort': sort_by,
         'status_options' :status_options,
    })

def add_job(request):
    if request.method=='POST':
        form=AddJobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Job added successfully")
            return redirect('job_list') #Redirect to job list after saving
        else:
            print("❌ Form is invalid:", form.errors)
    else:
        form=AddJobForm()

    return render(request, 'tracker/add_job.html', {'form': form})

def job_detail(request, pk):
# Tries to get the job with the given ID. If not found, shows a 404 error page.
    job = get_object_or_404(JobApplication, pk=pk)
 # Renders the job_detail.html template and passes the job data to it
    return render(request, 'tracker/job_detail.html', {'job': job})

def edit_job(request, pk):
    job = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
# Populate form with submitted data and link it to the existing job
        form = AddJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_detail', pk=job.pk)
    else:
        form = AddJobForm(instance=job)  # If GET request, pre-fill the form with the existing job's data
    return render(request, 'tracker/edit_job.html', {'form': form})


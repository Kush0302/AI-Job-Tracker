from django.shortcuts import render, redirect #render() combines a template with context data and returns an HTML response to the browser

from .models import JobApplication
from .forms import AddJobForm
from django.contrib import messages

def job_list(request):#request is a built-in object that represents the HTTP request sent by the browser
    jobs=JobApplication.objects.all()
    return render(request, 'tracker/job_list.html',{'jobs': jobs})

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


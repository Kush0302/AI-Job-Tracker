from django.shortcuts import render #render() combines a template with context data and returns an HTML response to the browser

from .models import JobApplication

def job_list(request):#request is a built-in object that represents the HTTP request sent by the browser
    jobs=JobApplication.objects.all()
    return render(request, 'tracker/job_list.html',{'jobs': jobs})

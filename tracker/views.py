from django.shortcuts import render, redirect, get_object_or_404 #render() combines a template with context data and returns an HTML response to the browser
from django.db.models import Q #Imports Django’s Q object, which allows combining multiple filter conditions with [OR] logic
from django.db.models import Count # useful for aggregating totals like how many jobs per status
from plotly.offline import plot
import plotly.graph_objs as go
from .models import JobApplication
from .forms import AddJobForm
from django.contrib import messages
from django.http import JsonResponse
import openai
from django.conf import settings
from dotenv import load_dotenv
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework import generics
from .serializers import JobApplicationSerializer
from tracker.models import JobApplication

class JobApplicationListCreateView(generics.ListCreateAPIView):
    queryset=JobApplication.objects.all()
    serializer_class=JobApplicationSerializer


def job_list(request): #request is a built-in object that represents the HTTP request sent by the browser
    status_filter=request.GET.get('status')
    sort_by=request.GET.get('sort', 'application_date')  #default sorting
    search_query=request.GET.get('search', '')


    jobs=JobApplication.objects.all()

#If a specific status is selected (not "All"), the queryset is filtered to show only jobs with that status
    if status_filter and status_filter!='All':
        jobs=jobs.filter(status=status_filter)

#Search Query 
    if search_query:
        jobs = jobs.filter(
        Q(company_name__icontains=search_query) |
        Q(position__icontains=search_query) #We use  __icontains to enable partial and case-insensitive matching
    )


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
        form=AddJobForm(request.POST, request.FILES)
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

def analytics_dashboard(request):
#values('status'): Creates a queryset grouped by the status field
#annotate(count=Count('status')): Adds a count field with how many times each status appears
    status_counts=JobApplication.objects.values('status').annotate(count=Count('status'))

    statuses=[entry['status'] for entry in status_counts]
    counts=[entry['count'] for entry in status_counts]


    bar_chart=go.Bar(x=statuses, y=counts, marker_color='indigo')
    layout=go.Layout(title="Job Application by Status",
                     xaxis=dict(title='Status'),
                     yaxis=dict(title="Count"))
    
#Combines the chart data (bar_chart) with layout to make a full Plotly figure object
    fig=go.Figure(data=[bar_chart], layout=layout)

#Converts the chart to a self-contained HTML <div> that can be embedded in Django template
    chart_div=plot(fig, output_type='div')

# Pie Chart
    pie_chart = go.Pie(labels=statuses, values=counts, hole=0.3)
    pie_layout = go.Layout(title='Status Distribution (Pie Chart)')
    pie_fig = go.Figure(data=[pie_chart], layout=pie_layout)
    pie_chart_div = plot(pie_fig, output_type='div')  # Embed pie chart as HTML <div>


# line Chart
    date_counts = JobApplication.objects.values('application_date').annotate(count=Count('id')).order_by('application_date')
    dates = [entry['application_date'].strftime('%Y-%m-%d') for entry in date_counts]
    date_counts_list = [entry['count'] for entry in date_counts]

    line_chart = go.Scatter(x=dates, y=date_counts_list, mode='lines+markers', line=dict(color='green'))
    line_layout = go.Layout(title="Applications Over Time",
                            xaxis=dict(title="Date"),
                            yaxis=dict(title="Number of Applications"))
    line_fig = go.Figure(data=[line_chart], layout=line_layout)
    line_div = plot(line_fig, output_type='div')

    return render(request, 'tracker/analytics.html', {
        'chart_div': chart_div,
        'pie_chart_div': pie_chart_div,
        'line_chart_div': line_div
    })

load_dotenv()

@csrf_exempt
def get_resume_feedback(request):
    print("METHOD:", request.method)
    if request.method != "POST":
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

    try:
        body = json.loads(request.body.decode("utf-8"))
        resume_text = body.get("resume_text", "").strip()
    except Exception:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if not resume_text:
        return JsonResponse({'error': 'resume_text is required'}, status=400)

    prompt = f"""
    You are an expert career coach and recruiter.

    Please review the following resume text and give concise feedback on improvements related to clarity, formatting, and relevance to technical roles.

    Resume:
    {resume_text}
    
    Be brief and actionable.
    """

    openai.api_key = settings.OPENROUTER_API_KEY
    openai.api_base = "https://openrouter.ai/api/v1"

    try:
        response = openai.ChatCompletion.create(
            model="cognitivecomputations/dolphin-mistral-24b-venice-edition:free",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7,
        )
        feedback = response["choices"][0]["message"]["content"]
        return JsonResponse({'feedback': feedback})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
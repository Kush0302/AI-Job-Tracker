from django.urls import path  # Imports the path() function to define routes
from .import views # Imports views from the current app
from .views import get_resume_feedback
from .views import JobApplicationListCreateView
from django.contrib.auth import views as auth_views

#path('jobs/') This maps the URL /jobs/ to your job_list view
#views.job_list Calls the view function you just wrote
#name='job_list' Useful for linking to this view later using Django’s template tags
urlpatterns=[path('', views.job_list, name='job_list'),
             path('add/', views.add_job, name='add_job'),
             path('job/<int:pk>/', views.job_detail, name='job_detail'), # URL for viewing details of one job 'pk'stands for(Primary Key)
             path('job/<int:pk>/edit/', views.edit_job, name='edit_job'), # URL for editing a job
             path('analytics/', views.analytics_dashboard, name="analytics"),
             path("get-resume-feedback/",get_resume_feedback, name="get_resume_feedback"),
             path("api/job-applications/", JobApplicationListCreateView.as_view(), name="job-applications"),
             path("job/<int:pk>/delete/", views.delete_job, name='delete_job'),
             path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
             path('logout/', auth_views.LogoutView.as_view(), name='logout'),
            ]
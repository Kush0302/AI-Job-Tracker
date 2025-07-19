from django.urls import path  # Imports the path() function to define routes
from .import views # Imports views from the current app

#path('jobs/') This maps the URL /jobs/ to your job_list view
#views.job_list Calls the view function you just wrote
#name='job_list' Useful for linking to this view later using Django’s template tags
urlpatterns=[path('', views.job_list, name='job_list'),
             path('add/', views.add_job, name='add_job'),
             path('job/<int:pk>/', views.job_detail, name='job_detail'), # URL for viewing details of one job 'pk'stands for(Primary Key)
             path('job/<int:pk>/edit/', views.edit_job, name='edit_job'), # URL for editing a job
             path('analytics/', views.analytics_dashboard, name="analytics"),
             path('get-resume-feedback/', views.get_resume_feedback, name="get_resume_feedback"),
            ]
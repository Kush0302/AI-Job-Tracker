from django.urls import path
from .import views

#path('jobs/') This maps the URL /jobs/ to your job_list view
#views.job_list Calls the view function you just wrote
#name='job_list' Useful for linking to this view later using Django’s template tags
urlpatterns=[path('', views.job_list, name='job_list'),
             path('add/', views.add_job, name='add_job'),
             ]
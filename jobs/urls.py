from django.urls import path
from . import views

urlpatterns = [
    path('post_job/', views.post_job, name='post_job'),
    path('job_list/', views.job_list, name='job_list'),
    path('job_search/', views.job_search, name='job_search'),
    path('job_alerts/', views.job_alerts, name='job_alerts'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
]
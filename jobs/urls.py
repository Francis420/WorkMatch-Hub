from django.urls import path, include
from . import views

app_name = "jobs"

urlpatterns = [
    path('post_job/', views.post_job, name='post_job'),
    path('posted_jobs/', views.posted_job, name='posted_job'),
    path('job_search/', views.job_search, name='job_search'),
    path('job_alerts/', views.job_alerts, name='job_alerts'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
    path('job/<int:job_id>/update/', views.update_job, name='update_job'),
    path('job/<int:job_id>/delete/', views.delete_job, name='delete_job'),
    path('jobs/<int:job_id>/cancel/', views.cancel_application, name='cancel_application'),
    path('hire/<int:application_id>/', views.hire_job_seeker, name='hire_job_seeker'),
    path('reject/<int:application_id>/', views.reject_job_seeker, name='reject_job_seeker'),
    path('jobs/<int:job_post_id>/applicant/<int:application_id>/', views.applicant_detail, name='applicant_detail'),

]
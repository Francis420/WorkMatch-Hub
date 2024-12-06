from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('register/job_seeker/', views.job_seeker_register, name='job_seeker_register'),
    path('register/employer/', views.employer_register, name='employer_register'),
    path('post_job/', views.post_job, name='post_job'),
    path('job_list/', views.job_list, name='job_list'),
    path('admin/suspend_user/<int:user_id>/', views.suspend_user, name='suspend_user'),
    path('admin/activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('admin/delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('job_search/', views.job_search, name='job_search'),
    path('job_alerts/', views.job_alerts, name='job_alerts'),
    path('candidate_search/', views.candidate_search, name='candidate_search'),
    path('set_notification_preferences/', views.set_notification_preferences, name='set_notification_preferences'),
    path('view_reports/', views.view_reports, name='view_reports'),
    path('report_issue/', views.report_issue, name='report_issue'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/job_seeker/', views.job_seeker_profile, name='job_seeker_profile'),
    path('profile/employer/', views.employer_profile, name='employer_profile'),  
    path('profile/', views.login_redirect, name='login_redirect'),
    path('profile/job_seeker/edit/', views.edit_job_seeker_profile, name='edit_job_seeker_profile'),
    path('profile/employer/edit/', views.edit_employer_profile, name='edit_employer_profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('candidate/<int:candidate_id>/', views.candidate_profile, name='candidate_profile'),
]

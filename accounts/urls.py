from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('register/job_seeker/', views.job_seeker_register, name='job_seeker_register'),
    path('register/employer/', views.employer_register, name='employer_register'),
    path('feedbacks/', views.view_feedbacks, name='view_feedbacks'),
    path('admin/suspend_user/<int:user_id>/', views.suspend_user, name='suspend_user'),
    path('admin/activate_user/<int:user_id>/', views.activate_user, name='activate_user'),
    path('set_notification_preferences/', views.set_notification_preferences, name='set_notification_preferences'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/job_seeker/<int:pk>/', views.job_seeker_profile, name='job_seeker_profile'),  
    path('profile/employer/<int:pk>/', views.employer_profile, name='employer_profile'),  
    path('profile/', views.login_redirect, name='login_redirect'),
    path('profile/job_seeker/edit/', views.edit_job_seeker_profile, name='edit_job_seeker_profile'),
    path('profile/employer/edit/', views.edit_employer_profile, name='edit_employer_profile'),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change-success/', TemplateView.as_view(template_name='accounts/password_change_success.html'), name='password_change_success'),
    path('create_admin/', views.create_admin, name='create_admin'),
    path('view_audit_logs/', views.view_audit_logs, name='view_audit_logs'),
    path('user_list/', views.user_list, name='user_list'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('resume/<int:profile_id>/', views.resume_view, name='view_resume'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

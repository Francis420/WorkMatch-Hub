from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from jobs.models import JobPost
import logging
from django.core.management.base import BaseCommand
from django.utils import timezone
from fuzzywuzzy import fuzz
from feedback.models import Feedback
from notifications.utils import notify
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import (
    JobSeekerSignUpForm, 
    EmployerSignUpForm, 
    NotificationPreferencesForm, 
    JobSeekerProfileForm, 
    EmployerProfileForm, 
    AdminCreationForm
)
from django.shortcuts import (
    render, 
    redirect, 
    get_object_or_404
)
from .models import (
    CustomUser, 
    Profile, 
    AuditLog,
)
from jobs.models import Application

User = get_user_model()
logger = logging.getLogger('workmatch_hub')



class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('password_change_success')

def log_user_activity(user, action):
    AuditLog.objects.create(user=user, action=action)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

@staff_member_required
def user_list(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    users = User.objects.all()

    if search_query:
        users = users.filter(username__icontains=search_query)

    if status_filter:
        if status_filter == 'active':
            users = users.filter(is_active=True)
        elif status_filter == 'inactive':
            users = users.filter(is_active=False)

    users = users.order_by('username')

    paginator = Paginator(users, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/user_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    })

@staff_member_required
def suspend_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    log_user_activity(request.user, f"suspended user {user.username}")
    return redirect('user_list')

@staff_member_required
def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    log_user_activity(request.user, f"activated user {user.username}")
    return redirect('user_list')

@staff_member_required
def create_admin(request):
    if request.method == 'POST':
        form = AdminCreationForm(request.POST)
        if form.is_valid():
            admin_user = form.save()
            log_user_activity(request.user, f"created admin {admin_user.username}")
            return redirect('admin:accounts_customuser_changelist')
    else:
        form = AdminCreationForm()
    return render(request, 'accounts/create_admin.html', {'form': form})

@staff_member_required
def view_audit_logs(request):
    search_query = request.GET.get('search', '')
    user_filter = request.GET.get('user', '')
    action_filter = request.GET.get('action', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    logs = AuditLog.objects.all()

    if user_filter:
        logs = logs.filter(user__username__icontains=user_filter)

    if action_filter:
        logs = logs.filter(action__icontains=action_filter)

    if start_date:
        start_date = parse_datetime(start_date)
        if start_date:
            start_date = timezone.make_aware(start_date)
            logs = logs.filter(timestamp__gte=start_date)

    if end_date:
        end_date = parse_datetime(end_date)
        if end_date:
            end_date = timezone.make_aware(end_date)
            logs = logs.filter(timestamp__lte=end_date)

    logs = logs.order_by('-timestamp')

    paginator = Paginator(logs, 10)  # number of results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/view_audit_logs.html', {
        'page_obj': page_obj,
        'user_filter': user_filter,
        'action_filter': action_filter,
        'start_date': start_date,
        'end_date': end_date,
    })

@staff_member_required
def view_feedbacks(request):
    search_query = request.GET.get('search', '')
    issue_type_filter = request.GET.get('issue_type', '')

    feedbacks = Feedback.objects.all()

    if search_query:
        feedbacks = feedbacks.filter(description__icontains=search_query)

    if issue_type_filter:
        feedbacks = feedbacks.filter(issue_type=issue_type_filter)

    feedbacks = feedbacks.order_by('-created_at')

    paginator = Paginator(feedbacks, 10)  # number of results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/view_feedbacks.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'issue_type_filter': issue_type_filter,
    })

def home(request):
    context = {
        'is_job_seeker': request.user.is_authenticated and request.user.is_job_seeker,
        'is_employer': request.user.is_authenticated and request.user.is_employer,
    }
    return render(request, 'home.html', context)

def register(request):
    return render(request, 'accounts/register.html')

def job_seeker_register(request):
    if request.method == 'POST':
        form = JobSeekerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_job_seeker = True
            user.save()
            login(request, user)
            return redirect('job_seeker_profile', pk=user.pk)
    else:
        form = JobSeekerSignUpForm()
    return render(request, 'accounts/job_seeker_register.html', {'form': form})

def employer_register(request):
    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_employer = True
            user.save()
            login(request, user)
            return redirect('employer_profile', pk=user.pk)
    else:
        form = EmployerSignUpForm()
    return render(request, 'accounts/employer_register.html', {'form': form})

@login_required
def set_notification_preferences(request):
    if request.method == 'POST':
        form = NotificationPreferencesForm(request.POST)
        if form.is_valid():
            request.user.profile.immediate_notifications = form.cleaned_data['immediate']
            request.user.profile.daily_notifications = form.cleaned_data['daily']
            request.user.profile.weekly_notifications = form.cleaned_data['weekly']
            request.user.profile.save()
            return redirect('set_notification_preferences')
    else:
        form = NotificationPreferencesForm(initial={
            'immediate': request.user.profile.immediate_notifications,
            'daily': request.user.profile.daily_notifications,
            'weekly': request.user.profile.weekly_notifications,
        })
    return render(request, 'accounts/set_notification_preferences.html', {'form': form})

def send_employer_notifications():
    job_posts = JobPost.objects.all()
    for job in job_posts:
        candidates = CustomUser.objects.filter(is_job_seeker=True)
        for candidate in candidates:
            skills_match = fuzz.partial_ratio(candidate.profile.skills.lower(), job.description.lower()) > 80
            if skills_match:
                message = f"A potential candidate matches your job posting: {candidate.username} with skills {candidate.profile.skills}"
                send_mail(
                    'New Candidate Alert',
                    message,
                    settings.EMAIL_HOST_USER,
                    [job.employer.email],
                    fail_silently=False,
                )

                # Create real-time notifications
                notify(
                    sender=candidate,
                    recipient=job.employer,
                    verb=f"New candidate match: {candidate.username} for your job posting {job.title}",
                    target=job
                )

class Command(BaseCommand):
    help = 'Send employer notifications'

    def handle(self, *args, **kwargs):
        from .views import send_employer_notifications
        send_employer_notifications()

@login_required
def job_seeker_profile(request, pk=None):
    if pk:
        user = get_object_or_404(CustomUser, pk=pk)
    else:
        user = request.user

    if user.is_job_seeker:
        profile = Profile.objects.get(user=user)
        applications = Application.objects.filter(user=user)
        return render(request, 'accounts/job_seeker_profile.html', {'profile': profile, 'applications': applications})
    else:
        return render(request, 'error.html', {'message': 'You are not authorized to view this page.'})

@login_required
def employer_profile(request, pk=None):
    if pk:
        user = get_object_or_404(CustomUser, pk=pk)
    else:
        user = request.user
    if user.is_employer:
        profile = Profile.objects.get(user=user)
        return render(request, 'accounts/employer_profile.html', {'profile': profile})
    else:
        return render(request, 'error.html', {'message': 'You are not authorized to view this page.'})

def login_redirect(request):
    user = request.user
    if user.is_authenticated:
        if user.is_job_seeker:
            return redirect('job_seeker_profile', pk=user.id)
        elif user.is_employer:
            return redirect('employer_profile', pk=user.id)
    return redirect('home')

@login_required
def edit_job_seeker_profile(request):
    user = request.user
    if user.is_job_seeker:
        profile, created = Profile.objects.get_or_create(user=user)
        
        if request.method == 'POST':
            form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('job_seeker_profile', pk=user.pk)
        else:
            form = JobSeekerProfileForm(instance=profile)
        
        return render(request, 'accounts/edit_job_seeker_profile.html', {'form': form})
    else:
        return render(request, 'error.html', {'message': 'You are not authorized to view this page.'})

@login_required
def edit_employer_profile(request):
    user = request.user
    if user.is_employer:
        profile, created = Profile.objects.get_or_create(user=user)
        if request.method == 'POST':
            form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('employer_profile', pk=user.pk)
        else:
            form = EmployerProfileForm(instance=profile)
        return render(request, 'accounts/edit_employer_profile.html', {'form': form})
    else:
        return render(request, 'error.html', {'message': 'You are not authorized to view this page.'})
    
def resume_view(request, profile_id):
    # Get the Profile object (the candidate's profile)
    profile = get_object_or_404(Profile, id=profile_id)
    
    if profile.resume:
        with open(profile.resume.path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="resume.pdf"'
            return response
    else:
        return HttpResponse("No Resume Uploaded", status=404)
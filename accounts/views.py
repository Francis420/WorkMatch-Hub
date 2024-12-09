from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import JobSeekerSignUpForm, EmployerSignUpForm, NotificationPreferencesForm, JobSeekerProfileForm, EmployerProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, Profile
import logging
from jobs.models import JobPost
from django.core.management.base import BaseCommand
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('profile')

User = get_user_model()
logger = logging.getLogger(__name__)

def home(request):
    context = {
        'is_job_seeker': request.user.is_authenticated and request.user.is_job_seeker,
        'is_employer': request.user.is_authenticated and request.user.is_employer,
    }
    return render(request, 'home.html', context)

@staff_member_required
def view_reports(request):
    with open('activity.log', 'r') as file:
        logs = file.readlines()
    return render(request, 'accounts/view_reports.html', {'logs': logs})

@staff_member_required
def suspend_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return redirect('admin:accounts_customuser_changelist')

@staff_member_required
def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    return redirect('admin:accounts_customuser_changelist')

@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin:accounts_customuser_changelist')

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
            return redirect('job_seeker_profile')
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
            return redirect('employer_profile')
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
            if candidate.profile.skills in job.description:
                message = f"A potential candidate matches your job posting: {candidate.username} with skills {candidate.profile.skills}"
                send_mail(
                    'New Candidate Alert',
                    message,
                    settings.EMAIL_HOST_USER,
                    [job.employer.email],
                    fail_silently=False,
                )

class Command(BaseCommand):
    help = 'Send employer notifications'

    def handle(self, *args, **kwargs):
        from .views import send_employer_notifications
        send_employer_notifications()

@login_required
def job_seeker_profile(request):
    user = request.user
    if user.is_job_seeker:
        profile = Profile.objects.get(user=user)
        return render(request, 'accounts/job_seeker_profile.html', {'profile': profile})
    else:
        return render(request, 'accounts/error.html', {'message': 'You are not authorized to view this page.'})

@login_required
def employer_profile(request):
    user = request.user
    if user.is_employer:
        profile = Profile.objects.get(user=user)
        return render(request, 'accounts/employer_profile.html', {'profile': profile})
    else:
        return render(request, 'accounts/error.html', {'message': 'You are not authorized to view this page.'})

def login_redirect(request):
    user = request.user
    if user.is_authenticated:
        if user.is_job_seeker:
            return redirect('job_seeker_profile')
        elif user.is_employer:
            return redirect('employer_profile')
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
                return redirect('job_seeker_profile')
        else:
            form = JobSeekerProfileForm(instance=profile)
        return render(request, 'accounts/edit_job_seeker_profile.html', {'form': form})
    else:
        return render(request, 'accounts/error.html', {'message': 'You are not authorized to view this page.'})

@login_required
def edit_employer_profile(request):
    user = request.user
    if user.is_employer:
        profile, created = Profile.objects.get_or_create(user=user)
        if request.method == 'POST':
            form = EmployerProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('employer_profile')
        else:
            form = EmployerProfileForm(instance=profile)
        return render(request, 'accounts/edit_employer_profile.html', {'form': form})
    else:
        return render(request, 'accounts/error.html', {'message': 'You are not authorized to view this page.'})
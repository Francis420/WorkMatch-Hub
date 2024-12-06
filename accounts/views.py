from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import JobSeekerSignUpForm, EmployerSignUpForm
from django.contrib.auth.decorators import login_required
from .forms import JobPostForm
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import JobPost
from .forms import JobSearchForm
from .forms import JobAlertForm
from .models import JobAlert
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from .forms import CandidateSearchForm
from .forms import NotificationPreferencesForm
from django.core.management.base import BaseCommand
import logging
from .forms import FeedbackForm
from .models import Profile
from .forms import JobSeekerProfileForm, EmployerProfileForm
from django.contrib.auth.models import User

User = get_user_model()
logger = logging.getLogger(__name__)

def candidate_profile(request, candidate_id):
    candidate = get_object_or_404(User, id=candidate_id)
    return render(request, 'candidate_profile.html', {'candidate': candidate})

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
    return render(request, 'view_reports.html', {'logs': logs})

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
    return render(request, 'register.html')

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
    return render(request, 'job_seeker_register.html', {'form': form})

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
    return render(request, 'employer_register.html', {'form': form})

@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job_post = form.save(commit=False)
            job_post.employer = request.user
            job_post.save()
            return redirect('job_list')
    else:
        form = JobPostForm()
    return render(request, 'post_job.html', {'form': form})

def job_search(request):
    form = JobSearchForm(request.GET or None)
    jobs = JobPost.objects.all()

    if form.is_valid():
        if form.cleaned_data['title']:
            jobs = jobs.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data['location']:
            jobs = jobs.filter(location__icontains=form.cleaned_data['location'])
        if form.cleaned_data['min_salary']:
            jobs = jobs.filter(salary__gte=form.cleaned_data['min_salary'])
        if form.cleaned_data['max_salary']:
            jobs = jobs.filter(salary__lte=form.cleaned_data['max_salary'])

    return render(request, 'job_search.html', {'form': form, 'jobs': jobs})

@login_required
def job_alerts(request):
    if request.method == 'POST':
        form = JobAlertForm(request.POST)
        if form.is_valid():
            job_alert = form.save(commit=False)
            job_alert.user = request.user
            job_alert.save()
            return redirect('job_alerts')
    else:
        form = JobAlertForm()
    return render(request, 'job_alerts.html', {'form': form})

def send_job_alerts():
    alerts = JobAlert.objects.all()
    for alert in alerts:
        jobs = JobPost.objects.all()
        if alert.job_title:
            jobs = jobs.filter(title__icontains=alert.job_title)
        if alert.location:
            jobs = jobs.filter(location__icontains=alert.location)
        if alert.industry:
            jobs = jobs.filter(industry__icontains=alert.industry)

        if jobs.exists():
            message = "Here are the latest job postings matching your preferences:\n"
            for job in jobs:
                message += f"{job.title} in {job.location} - {job.salary}\n"
            send_mail(
                'Job Alerts',
                message,
                settings.EMAIL_HOST_USER,
                [alert.user.email],
                fail_silently=False,
            )

def candidate_search(request):
    form = CandidateSearchForm(request.GET or None)
    candidates = CustomUser.objects.filter(is_job_seeker=True)

    if form.is_valid():
        if form.cleaned_data['qualifications']:
            candidates = candidates.filter(profile__qualifications__icontains=form.cleaned_data['qualifications'])
        if form.cleaned_data['skills']:
            candidates = candidates.filter(profile__skills__icontains=form.cleaned_data['skills'])
        if form.cleaned_data['location']:
            candidates = candidates.filter(profile__location__icontains=form.cleaned_data['location'])

    return render(request, 'candidate_search.html', {'form': form, 'candidates': candidates})

@login_required
def set_notification_preferences(request):
    if request.method == 'POST':
        form = NotificationPreferencesForm(request.POST)
        if form.is_valid():
            # Save the preferences to the user's profile or a related model
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
    return render(request, 'set_notification_preferences.html', {'form': form})

def send_employer_notifications():
    job_posts = JobPost.objects.all()
    for job in job_posts:
        candidates = CustomUser.objects.filter(is_job_seeker=True)
        for candidate in candidates:
            # Check if candidate matches job criteria (this is a simplified example)
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
def report_issue(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('report_issue')
    else:
        form = FeedbackForm()
    return render(request, 'report_issue.html', {'form': form})

def job_list(request):
    job_posts = JobPost.objects.all()
    return render(request, 'job_list.html', {'job_posts': job_posts})

@login_required
def job_seeker_profile(request):
    user = request.user
    if user.is_job_seeker:
        profile = Profile.objects.get(user=user)
        return render(request, 'job_seeker_profile.html', {'profile': profile})
    else:
        return render(request, 'error.html', {'message': 'You are not authorized to view this page.'})

@login_required
def employer_profile(request):
    user = request.user
    if user.is_employer:
        profile = Profile.objects.get(user=user)
        return render(request, 'employer_profile.html', {'profile': profile})
    else:
        return render(request, 'error.html', {'message': 'You are not authorized to view this page.'})

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
        return render(request, 'edit_job_seeker_profile.html', {'form': form})
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
                return redirect('employer_profile')
        else:
            form = EmployerProfileForm(instance=profile)
        return render(request, 'edit_employer_profile.html', {'form': form})
    else:
        return render(request, 'error.html', {'message': 'You are not authorized to view this page.'})
    
def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    return render(request, 'job_detail.html', {'job': job})
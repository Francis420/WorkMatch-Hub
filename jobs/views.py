from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobPostForm, JobSearchForm, JobAlertForm
from .models import JobAlert, JobPost
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.models import AuditLog  # Import AuditLog from accounts app
import logging
from fuzzywuzzy import fuzz
from notifications.utils import notify
from .models import Application

User = get_user_model()
logger = logging.getLogger('workmatch_hub')

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
    return render(request, 'jobs/post_job.html', {'form': form})

def job_list(request):
    job_posts = JobPost.objects.all()
    return render(request, 'jobs/job_list.html', {'job_posts': job_posts})

def job_search(request):
    form = JobSearchForm(request.GET or None)
    jobs = JobPost.objects.all()

    if form.is_valid():
        user = request.user
        search_params = []

        if form.cleaned_data['title']:
            jobs = jobs.filter(title__icontains=form.cleaned_data['title'])
            search_params.append(f"title: {form.cleaned_data['title']}")
        if form.cleaned_data['location']:
            jobs = jobs.filter(location__icontains=form.cleaned_data['location'])
            search_params.append(f"location: {form.cleaned_data['location']}")
        if form.cleaned_data['min_salary']:
            jobs = jobs.filter(salary__gte=form.cleaned_data['min_salary'])
            search_params.append(f"min_salary: {form.cleaned_data['min_salary']}")
        if form.cleaned_data['max_salary']:
            jobs = jobs.filter(salary__lte=form.cleaned_data['max_salary'])
            search_params.append(f"max_salary: {form.cleaned_data['max_salary']}")

        # Log the search query
        if user.is_authenticated:
            search_query = ", ".join(search_params) if search_params else "No search parameters"
            logger.info(f"User {user.username} searched for: {search_query}")
            AuditLog.objects.create(user=user, action=f"searched for: {search_query}")

    return render(request, 'jobs/job_search.html', {'form': form, 'jobs': jobs})

def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

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
    return render(request, 'jobs/job_alerts.html', {'form': form})

def send_job_alerts():
    alerts = JobAlert.objects.all()
    for alert in alerts:
        jobs = JobPost.objects.all()
        matching_jobs = []

        for job in jobs:
            title_match = fuzz.partial_ratio(alert.job_title.lower(), job.title.lower()) > 80 if alert.job_title else True
            location_match = fuzz.partial_ratio(alert.location.lower(), job.location.lower()) > 80 if alert.location else True
            industry_match = fuzz.partial_ratio(alert.industry.lower(), job.industry.lower()) > 80 if alert.industry else True

            if title_match or location_match or industry_match:
                matching_jobs.append(job)

        if matching_jobs:
            message = "Here are the latest job postings matching your preferences:\n"
            for job in matching_jobs:
                message += f"{job.title} in {job.location} - {job.salary}\n"
            send_mail(
                'Job Alerts',
                message,
                settings.EMAIL_HOST_USER,
                [alert.user.email],
                fail_silently=False,
            )

def apply_for_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    user = request.user

    if user.is_job_seeker:
        # Save the application in the database
        Application.objects.create(job_post=job, user=user)

        # Send email notification to the employer
        message = f"{user.username} has applied for your job posting: {job.title}"
        send_mail(
            'Job Application Received',
            message,
            settings.EMAIL_HOST_USER,
            [job.employer.email],
            fail_silently=False,
        )

        # Create a notification
        notification = notify(sender=user, recipient=job.employer, verb=message, target=job)
        print(f"Notification created: {notification}, Sender: {notification.sender}, Sender ID: {notification.sender.id}")

        return redirect('job_detail', job_id=job.id)
    else:
        return render(request, 'accounts/error.html', {'message': 'You are not authorized to apply for this job.'})
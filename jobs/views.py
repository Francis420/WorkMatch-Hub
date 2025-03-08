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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from django.utils import timezone
from datetime import timedelta
from notifications.models import Notification
from django.db.models import Q

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
            send_job_alerts()  # Call the function to send job alerts
            return redirect('posted_job')
    else:
        form = JobPostForm()
    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def update_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    if request.method == 'POST':
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('posted_job')
    else:
        form = JobPostForm(instance=job)
    return render(request, 'jobs/update_job.html', {'form': form})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    if request.method == 'POST':
        job.delete()
        return redirect('posted_job')
    return render(request, 'jobs/delete_job.html', {'job': job})

def posted_job(request):
    user = request.user
    query = request.GET.get('q', '') 
    if query:
        job_posts = JobPost.objects.filter(
            Q(employer=user) & (Q(title__icontains=query) | Q(description__icontains=query))
        ).order_by('-created_at')
    else:
        job_posts = JobPost.objects.filter(employer=user).order_by('-created_at')
    return render(request, 'jobs/posted_job.html', {'job_posts': job_posts, 'query': query})

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
    user = request.user
    can_apply = True
    reapply_time = None

    if user.is_authenticated and user.is_job_seeker:
        recent_application = Application.objects.filter(job_post=job, user=user, timestamp__gte=timezone.now() - timedelta(days=1)).first()
        if recent_application:
            can_apply = False
            reapply_time = recent_application.timestamp + timedelta(days=1)

    context = {
        'job': job,
        'can_apply': can_apply,
        'reapply_time': reapply_time,
        'user_has_applied': Application.objects.filter(job_post=job, user=user).exists()
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def job_alerts(request):
    try:
        job_alert = JobAlert.objects.get(user=request.user)
    except JobAlert.DoesNotExist:
        job_alert = None

    if request.method == 'POST':
        form = JobAlertForm(request.POST, instance=job_alert)
        if form.is_valid():
            job_alert = form.save(commit=False)
            job_alert.user = request.user
            job_alert.save()
            return redirect('job_alerts')
    else:
        form = JobAlertForm(instance=job_alert)

    return render(request, 'jobs/job_alerts.html', {'form': form})

def send_job_alerts():
    alerts = JobAlert.objects.all()

    for alert in alerts:
        jobs = JobPost.objects.all()
        matching_jobs = {}

        for job in jobs:
            # Skip jobs that have already been notified
            if job.id in alert.notified_jobs:
                continue

            # Use exact match for location
            location_match = alert.location.lower() == job.location.lower() if alert.location else True

            # Use TF-IDF and cosine similarity for job title and description
            vectorizer = TfidfVectorizer().fit_transform([alert.job_title, job.title, alert.job_description, job.description])
            vectors = vectorizer.toarray()
            title_similarity = cosine_similarity([vectors[0]], [vectors[1]])[0][0] if alert.job_title else 1
            description_similarity = cosine_similarity([vectors[2]], [vectors[3]])[0][0] if alert.job_description else 1

            # Define a threshold for similarity
            title_threshold = 0.8
            description_threshold = 0.8

            title_match = title_similarity >= title_threshold
            description_match = description_similarity >= description_threshold

            if location_match or title_match or description_match:
                match_details = []
                if title_match:
                    match_details.append("title")
                if description_match:
                    match_details.append("description")
                if location_match:
                    match_details.append("location")
                match_details_str = ", ".join(match_details)

                if job not in matching_jobs:
                    matching_jobs[job] = match_details_str
                else:
                    existing_match_details = matching_jobs[job].split(", ")
                    combined_match_details = list(set(existing_match_details + match_details))
                    matching_jobs[job] = ", ".join(combined_match_details)

        if matching_jobs:
            message = "Here are the latest job postings matching your preferences:\n"
            for job, match_details_str in matching_jobs.items():
                message += f"{job.title} in {job.location} - {job.salary} (matched on: {match_details_str})\n"
            send_mail(
                'Job Alerts',
                message,
                settings.EMAIL_HOST_USER,
                [alert.user.email],
                fail_silently=False,
            )

            # Create real-time notifications
            for job, match_details_str in matching_jobs.items():
                if job.id not in alert.notified_jobs:
                    if not Notification.objects.filter(sender=job.employer, recipient=alert.user, verb=f"New job alert: {job.title} in {job.location} (matched on: {match_details_str})", target=job).exists():
                        notification = notify(
                            sender=job.employer,
                            recipient=alert.user,
                            verb=f"New job alert: {job.title} in {job.location} (matched on: {match_details_str})",
                            target=job
                        )
                        logger.info(f"Notification created: {notification}, Recipient: {alert.user.username}, Job: {job.title}")
                        alert.notified_jobs.append(job.id)
                        alert.save()
                else:
                    logger.info(f"Notification already exists for user: {alert.user.username}, Job: {job.title}")

@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    user = request.user

    if user.is_job_seeker:
        # Check if the user has applied within the last 24 hours
        recent_application = Application.objects.filter(job_post=job, user=user, timestamp__gte=timezone.now() - timedelta(days=1)).exists()
        if recent_application:
            return render(request, 'accounts/error.html', {'message': 'You cannot reapply for this job within 24 hours of your last application or cancellation.'})

        # Save the application in the database
        Application.objects.create(job_post=job, user=user, timestamp=timezone.now())

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
        if not Notification.objects.filter(sender=user, recipient=job.employer, verb=message, target=job).exists():
            notification = notify(sender=user, recipient=job.employer, verb=message, target=job)
            print(f"Notification created: {notification}, Sender: {notification.sender}, Sender ID: {notification.sender.id}")

        return redirect('job_detail', job_id=job.id)
    else:
        return render(request, 'accounts/error.html', {'message': 'Please Try Again Later.'})
    
@login_required
def cancel_application(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    user = request.user

    if user.is_job_seeker:
        applications = Application.objects.filter(job_post=job, user=user)
        if applications.exists():
            for application in applications:
                application.delete()
            message = f"{user.username} has cancelled their application(s) for your job posting: {job.title}"
            send_mail('Job Application Cancelled', message, settings.EMAIL_HOST_USER, [job.employer.email], fail_silently=False)
            notify(sender=user, recipient=job.employer, verb=message, target=job)
            return redirect('job_detail', job_id=job.id)
        else:
            return render(request, 'accounts/error.html', {'message': 'No applications found to cancel.'})
    else:
        return render(request, 'accounts/error.html', {'message': 'You are not authorized to cancel this application.'})
    


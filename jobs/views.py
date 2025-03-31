from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobPostForm, JobSearchForm, JobAlertForm
from .models import JobAlert, JobPost
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import get_user_model
from accounts.models import AuditLog  
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
from django.core.paginator import Paginator
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime


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
            return redirect('jobs:posted_job')
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
            return redirect('jobs:posted_job')
    else:
        form = JobPostForm(instance=job)
    return render(request, 'jobs/update_job.html', {'form': form})

@login_required
def delete_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    if request.method == 'POST':
        job.delete()
        return redirect('jobs:posted_job')
    return render(request, 'jobs/delete_job.html', {'job': job})

@login_required
def posted_job(request):
    user = request.user
    query = request.GET.get('q', '')

    job_posts = JobPost.objects.filter(employer=user).order_by('-created_at')  # Sort by newest first

    if query:
        job_posts = job_posts.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    paginator = Paginator(job_posts, 10)  # Show 10 job posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/posted_job.html', {
        'page_obj': page_obj,
        'query': query,
    })


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

    paginator = Paginator(jobs, 3)  # Number of results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/job_search.html', {'form': form, 'page_obj': page_obj})

def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    user = request.user
    hired = False
    hired_date = None
    rejected = False
    reapply_time = None
    pending = False
    pending_since = None

    # Get the latest application for this job by the user
    application = Application.objects.filter(job_post=job, user=user).order_by('-timestamp').first()

    if application:
        if application.status == "hired":
            hired = True
            hired_date = application.timestamp  # Application timestamp for hired date

        elif application.status == "rejected":
            rejected = True
            reapply_time = application.timestamp + timedelta(days=180)  # Cooldown of 180 days (6 months)

        elif application.status == "pending":
            pending = True
            pending_since = application.timestamp  # Track when the user applied

    context = {
        "job": job,
        "hired": hired,
        "hired_date": hired_date,
        "rejected": rejected,
        "reapply_time": reapply_time,
        "pending": pending,
        "pending_since": pending_since,
    }
    return render(request, "jobs/job_detail.html", context)


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
    job_post = get_object_or_404(JobPost, id=job_id)
    user = request.user

    # Check for previous applications
    previous_application = Application.objects.filter(job_post=job_post, user=user).order_by('-timestamp').first()

    if previous_application:
        # Enforce cooldown based on last application timestamp
        cooldown_period = timedelta(days=180)
        if timezone.now() - previous_application.timestamp < cooldown_period:
            return render(request, 'error.html', {
                "error_message": "You have already applied for this job. Please wait 6 months before reapplying."
            })

    # Create a new application
    application = Application.objects.create(job_post=job_post, user=user, status="pending")

    # Manually create a Notification instead of using notify()
    Notification.objects.create(
        sender=user,
        recipient=job_post.employer,
        verb=f"{user.username} has applied for {job_post.title} at {job_post.location}.",
        target=job_post,
        extra_data={
        "application_id": application.id,
        "job_id": job_post.id,  
        "applied_timestamp": str(application.timestamp)
    }
    )

    return redirect('jobs:job_detail', job_id=job_post.id)

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
            return redirect('jobs:job_detail', job_id=job.id)
        else:
            return render(request, 'error.html', {'message': 'No applications found to cancel.'})
    else:
        return render(request, 'error.html', {'message': 'You are not authorized to cancel this application.'})

@login_required
def hire_job_seeker(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    job_post = application.job_post

    if job_post.remaining_slots > 0 and application.status in ['pending', 'rejected']:  # Allow hiring even if previously rejected
        application.status = 'hired'
        application.timestamp = timezone.now()  # Update timestamp for tracking
        job_post.remaining_slots -= 1
        job_post.save()
        application.save()

        # Retrieve existing extra_data and update only necessary fields
        notification, created = Notification.objects.update_or_create(
            sender=request.user,
            recipient=application.user,
            target=job_post,
            verb=f"You have been hired for {job_post.title} at {job_post.location}.",
            defaults={"extra_data": {}}
        )

        # Preserve existing data and update only necessary fields
        notification.extra_data = {
            **(notification.extra_data if notification.extra_data else {}),  # Preserve previous data
            "latest_action": "hired",
            "latest_timestamp": str(application.timestamp),  # Store latest timestamp
        }
        notification.save()

        print(f"Notification Updated: {notification}, Extra Data: {notification.extra_data}")

        return redirect('jobs:applicant_detail', job_post_id=job_post.id, application_id=application.id)

    else:
        notify(
            sender=request.user,
            recipient=application.user,
            verb=f"You have been hired for {job_post.title} at {job_post.location}, but an error occurred.",
            target=job_post
        )

    return redirect('jobs:applicant_detail', job_post_id=job_post.id, application_id=application.id)

@login_required
def reject_job_seeker(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    job_post = application.job_post

    was_hired = application.status == 'hired'

    if application.status in ['pending', 'hired']:  
        application.status = 'rejected'
        application.timestamp = timezone.now()  
        application.save()

        if was_hired:
            job_post.remaining_slots += 1
            job_post.save()

        # ✅ Fetch the existing notification (if any) before using it
        notification = Notification.objects.filter(
            recipient=application.user,
            target=job_post
        ).order_by('-timestamp').first()  # Get the latest notification

        # ✅ Now `notification` exists, so we can safely preserve extra_data
        Notification.objects.update_or_create(
            sender=request.user,
            recipient=application.user,
            target=application.job_post,
            verb=f"You have been rejected for {application.job_post.title} at {application.job_post.location}.",
            defaults={
                "extra_data": {
                    **(notification.extra_data if notification and notification.extra_data else {}),  
                    "application_id": application.id,
                    "job_id": application.job_post.id,
                    "latest_action": "rejected",
                    "latest_timestamp": str(application.timestamp)
                }
            }
        )

        return redirect('jobs:applicant_detail', job_post_id=application.job_post.id, application_id=application.id)

    elif application.status == 'rejected':
        return render(request, 'error.html', {
            "error_message": "This application has already been rejected."
        })

    return render(request, 'error.html', {
        "error_message": "An error occurred while processing the rejection. Please contact support."
    })

@login_required
def applicant_detail(request, job_post_id, application_id):
    print(f"Job Post ID: {job_post_id}, Application ID: {application_id}") #remove later, just to debug
    job_post = get_object_or_404(JobPost, id=job_post_id)
    application = get_object_or_404(Application, id=application_id, job_post=job_post)

    return render(request, 'jobs/applicant_detail.html', {
        'job_post': job_post,
        'application': application,
        'applicant': application.user 
    })

    


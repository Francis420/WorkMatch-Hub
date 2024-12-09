from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobPostForm, JobSearchForm, JobAlertForm
from .models import JobAlert, JobPost
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

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
        if form.cleaned_data['title']:
            jobs = jobs.filter(title__icontains=form.cleaned_data['title'])
        if form.cleaned_data['location']:
            jobs = jobs.filter(location__icontains=form.cleaned_data['location'])
        if form.cleaned_data['min_salary']:
            jobs = jobs.filter(salary__gte=form.cleaned_data['min_salary'])
        if form.cleaned_data['max_salary']:
            jobs = jobs.filter(salary__lte=form.cleaned_data['max_salary'])

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
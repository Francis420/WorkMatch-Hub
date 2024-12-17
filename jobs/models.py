from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()
class JobPost(models.Model):
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('freelance', 'Freelance'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
        ('one_time', 'One-Time Task'),
    ]

    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    job_duration = models.CharField(max_length=255, blank=True, null=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, default='contract')
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.title


class JobAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    job_description = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notified_jobs = models.JSONField(default=list)

    def __str__(self):
        return f"{self.user.username}'s Job Alert"

class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job_post = models.ForeignKey('JobPost', on_delete=models.CASCADE)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.job_post.title}"
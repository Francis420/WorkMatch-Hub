from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    is_job_seeker = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    company_name = models.CharField(max_length=255, blank=True, null=True)

def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    immediate_notifications = models.BooleanField(default=False)
    daily_notifications = models.BooleanField(default=False)
    weekly_notifications = models.BooleanField(default=False)
    
    # Job Seeker specific fields
    full_name = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True, validators=[validate_pdf])
    location = models.CharField(max_length=255, blank=True, null=True)
    availability = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True) 

    # Employer specific fields
    employer_name = models.CharField(max_length=255, blank=True, null=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    industry = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    is_small_scale = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
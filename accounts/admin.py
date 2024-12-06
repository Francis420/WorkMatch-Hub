# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, JobPost, JobAlert, Profile, Feedback

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_job_seeker', 'is_employer', 'is_active']
    list_filter = ['is_job_seeker', 'is_employer', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Roles', {'fields': ('is_job_seeker', 'is_employer', 'company_name')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(JobPost)
admin.site.register(JobAlert)
admin.site.register(Profile)
admin.site.register(Feedback)

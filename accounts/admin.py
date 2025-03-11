from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, AuditLog
from feedback.models import Feedback
from jobs.models import JobPost, JobAlert

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 
                    'email', 
                    'is_active', 
                    'is_staff', 
                    'is_job_seeker', 
                    'is_employer')
    actions = ['activate_users', 'deactivate_users']

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Deactivate selected users"

admin.site.register(AuditLog)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Feedback)
admin.site.register(JobPost)
admin.site.register(JobAlert)

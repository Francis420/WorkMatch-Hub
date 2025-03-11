from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'verb', 'target', 'read', 'timestamp')
    list_filter = ('read', 'timestamp')
    search_fields = ('recipient__username', 'verb', 'target__title')

admin.site.register(Notification, NotificationAdmin)
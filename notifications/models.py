from django.conf import settings
from django.db import models

class Notification(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        null=True,
        blank=True
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    verb = models.CharField(max_length=255)
    target = models.ForeignKey('jobs.JobPost', on_delete=models.CASCADE, null=True, blank=True)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    extra_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f'Notification for {self.recipient} - {self.verb}'

    def mark_as_read(self):
        self.read = True
        self.save()

    def mark_as_unread(self):
        self.read = False
        self.save()

    @property
    def parsed_extra_data(self):
        return self.extra_data or {}
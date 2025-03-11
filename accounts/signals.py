from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile
import logging
from django.contrib.auth import get_user_model
from .models import AuditLog
from django.contrib.auth.signals import (
    user_logged_in, 
    user_logged_out
)

logger = logging.getLogger('workmatch_hub')
User = get_user_model()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f"User logged in: {user.username}")
    AuditLog.objects.create(user=user, action="logged in")

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user and user.is_authenticated:
        logger.info(f"User logged out: {user.username}")
        AuditLog.objects.create(user=user, action="logged out")
    else:
        logger.info('An anonymous user has logged out.')

@receiver(post_save, sender=User)
def log_user_profile_update(sender, instance, created, **kwargs):
    if not created:
        logger.info(f"User updated profile: {instance.username}")
        AuditLog.objects.create(user=instance, action="updated profile")
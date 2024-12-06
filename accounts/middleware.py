import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class ActivityLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            logger.info(f'User {request.user.username} accessed {request.path}')

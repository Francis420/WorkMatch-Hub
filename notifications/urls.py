from django.urls import path
from .views import notifications_view, mark_read, mark_unread

urlpatterns = [
    path('', notifications_view, name='notifications'),
    path('mark_read/<int:notification_id>/', mark_read, name='mark_read'),
    path('mark_unread/<int:notification_id>/', mark_unread, name='mark_unread'),
]
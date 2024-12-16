from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications_view, name='notifications'),
    path('mark_read/<int:pk>/', views.mark_notification_as_read, name='mark_read'),
]
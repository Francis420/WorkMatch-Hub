from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'notifications/notifications.html', {'notifications': notifications})

@login_required
@require_POST
def mark_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)

@login_required
@require_POST
def mark_unread(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.read = False
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)
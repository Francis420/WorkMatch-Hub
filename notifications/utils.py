from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def notify(sender, recipient, verb, target=None):
    notification = Notification.objects.create(
        sender=sender,
        recipient=recipient,
        verb=verb,
        target=target
    )
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{recipient.id}",
        {
            "type": "send_notification",
            "message": verb
        }
    )
    return notification
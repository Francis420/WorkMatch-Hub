import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger('workmatch_hub')

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.user = self.scope["user"]
            self.group_name = f"notifications_{self.user.id}"

            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )

            await self.accept()
            logger.info(f"WebSocket connected for user: {self.user.username}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        logger.info(f"WebSocket disconnected for user: {self.user.username}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_notification",
                "message": message
            }
        )

    async def send_notification(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({
            "message": message
        }))
        logger.info(f"Notification sent to user: {self.user.username}, Message: {message}")
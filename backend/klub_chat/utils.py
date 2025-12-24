# klub_chat/utils.py
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async

from .models import MeetingAlert

async def send_meeting_alert(title, started_at, meeting_id):
    exists = await sync_to_async(MeetingAlert.objects.filter(meeting_id=meeting_id).exists)()
    if exists:
        return
    await sync_to_async(MeetingAlert.objects.create)(meeting_id=meeting_id)

    channel_layer = get_channel_layer()
    if channel_layer:
        await channel_layer.group_send(
            "meeting_alerts",
            {
                "type": "send_meeting_alert",
                "title": title,
                "started_at": started_at.strftime('%Y-%m-%d %H:%M:%S'),
                "meeting_id": meeting_id
            }
        )

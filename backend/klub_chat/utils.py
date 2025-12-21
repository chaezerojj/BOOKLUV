

from channels.layers import get_channel_layer

def send_meeting_alert(title, started_at):
    channel_layer = get_channel_layer()
    channel_layer.group_send(
        'meeting_alerts',  # 모든 클라이언트에게 전송
        {
            'type': 'send_meeting_alert',
            'title': title,
            'started_at': started_at
        }
    )

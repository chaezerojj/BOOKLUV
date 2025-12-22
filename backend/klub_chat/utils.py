

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_meeting_alert(title, started_at):
    # WebSocket 그룹에 메시지를 보내기
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "meeting_alerts",  # WebSocket 그룹 이름
        {
            "type": "send_meeting_alert",  # 클라이언트에서 처리할 이벤트 타입
            "title": title,
            "started_at": started_at.strftime('%Y-%m-%d %H:%M:%S'),  # 알림 시간
        }
    )
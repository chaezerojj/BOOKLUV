from django.shortcuts import render
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse

# 1. 알람 확인용 테스트 페이지 렌더링
def alarm_test_page(request):
    return render(request, 'alrams/test.html')

# 2. 이 함수가 호출되면 실제로 웹소켓 신호를 보냄
def trigger_alarm(request):
    channel_layer = get_channel_layer()
    # 특정 유저(현재 접속자) 그룹에 신호 전송
    group_name = f"user_{request.user.id}"
    
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "alarm_message", # consumers.py의 메서드 이름
            "content": {
                "action": "ACTIVATE_5MIN_ALARM",
                "message": "신호가 정상적으로 도착했습니다!"
            }
        }
    )
    return JsonResponse({"status": "Success", "target": group_name})
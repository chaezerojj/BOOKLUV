# klub_chat/urls.py
from django.urls import path
from . import views
from . import api_views

app_name = "chat"

urlpatterns = [
    # 알람(JSON) - 기존 유지
    path("alarms/", views.today_meetings, name="today-meetings"),

    # HTML(백엔드 확인용) - 기존 유지
    path("rooms/", views.room_list, name="room-list"),
    path("rooms/<slug:room_name>/", views.room_detail, name="room-detail"),

    # Vue용 JSON API 추가
    path("api/rooms/", api_views.rooms_api, name="rooms-api"),
    path("api/rooms/<slug:room_slug>/", api_views.room_detail_api, name="room-detail-api"),
    # 알람 로그 (사용자별)
    path("api/alarms/logs/", api_views.alarms_logs_api, name="alarms-logs-api"),
]
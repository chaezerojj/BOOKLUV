from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 관리자
    path('admin', admin.site.urls),
    # 책, 모임, 퀴즈 CRUD
    path('api/v1/', include('klub_talk.urls')), 
    # 웹소켓 실시간 채팅 CRUD
    path('api/chat/', include('klub_chat.urls')), 
    # AI API 기반 추천 기능 
    path("api/recommend/", include("klub_recommend.urls")),
    # 웹소켓 실시간 알림 기능
    path("api/alarm/", include("klub_alarm.urls")),
    path("api/auth/", include('klub_user.urls'))
]

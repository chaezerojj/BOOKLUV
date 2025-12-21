from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import HttpResponse

def home(request):
    return HttpResponse("로그인 성공 🎉") #임시 메인페이지 대체

urlpatterns = [
    path("", home), #임시
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
    path("api/auth/", include('klub_user.urls')),
    path(
        "auth/callback/",
        TemplateView.as_view(template_name="auth/callback.html"),
        name="auth-callback-page",
    ),
]


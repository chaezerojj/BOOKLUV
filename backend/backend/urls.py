from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="BOOKLUV API",
        default_version="v1",
        description="BOOKLUV 백엔드 API 문서",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

def home(request):
    return HttpResponse("로그인 성공!") #임시 메인페이지 대체

urlpatterns = [
    # 관리자
    path('admin/', admin.site.urls),
    # login
    path("api/v1/auth/", include('klub_user.urls')),
    path("auth/v1/callback/",
    TemplateView.as_view(template_name="auth/callback.html"), name="auth-callback-page"),
    
    # path('api/v1/board/', include('klub_board.urls', namespace='board')),
    path('api/v1/board/', include('klub_board.api_urls', namespace='board')),
    # 책, 모임 정보
    path("api/v1/books/", include("klub_talk.api_urls")),
    # 테스트
    path("api/v1/book/", include("klub_talk.urls")),
    # 실시간 채팅 정보
    path("api/v1/chat/", include("klub_chat.urls")),
    # AI API 추천 정보
    path("api/v1/recommendations/", include("klub_recommend.urls")),

    # ===== Swagger =====
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
]

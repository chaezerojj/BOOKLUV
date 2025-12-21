from django.contrib import admin
from django.urls import path, include
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

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # ===== API v1 =====
    # 1. 책, 모임 정보
    path("api/v1/books/", include("klub_talk.urls")),
    # 2. 실시간 채팅 정보
    path("api/v1/chat/", include("klub_chat.urls")),
    # 3. AI API 추천 정보
    path("api/v1/recommendations/", include("klub_recommend.urls")),
    # 4. 사용자 로그인/로그아웃 정보
    path("api/v1/auth/", include("klub_user.urls")),

    # ===== Swagger =====
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
]

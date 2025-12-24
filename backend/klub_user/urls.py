from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = "auth"

urlpatterns = [
    path("", views.auth_login, name="login"),
    path("callback/", views.kakao_callback, name="callback"),

    # ✅ 프론트용
    path("me/", views.me, name="me"),
    path("logout/", views.logout_view, name="logout"),

    # (템플릿 페이지)
    path("mypage/", views.mypage, name="mypage"),
    path("mypage/edit/", views.mypage_edit, name="mypage_edit"),
    path("myroom/", views.myroom, name="myroom"),
    
    path("csrf/", views.csrf, name="csrf"),
]
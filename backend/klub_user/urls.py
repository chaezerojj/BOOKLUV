from django.urls import path
from . import views
from django.views.generic import TemplateView
# from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = 'user'

urlpatterns = [
    path('', views.auth_login, name='login'),
    path('callback/', views.kakao_callback, name='callback'),  # 수정!

    path("mypage/", views.mypage, name="mypage"),
    path("mypage/rooms/", views.myroom, name="myroom"),
    path("mypage/edit/", views.mypage_edit, name="mypage_edit"),
    # path("token/refresh/", views.token_refresh, name="token_refresh"),
    # path("logout/", views.logout, name="logout"), 
]
    # path('kakao/login/finish/', KakaoLogin.as_view(), name='login_to_django'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # #path("callback/", TemplateView.as_view(template_name="auth/callback.html")),

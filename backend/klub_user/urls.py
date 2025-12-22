from django.urls import path
from . import views
from django.views.generic import TemplateView
# from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = 'klub_user'

urlpatterns = [
    path('', views.login, name='login'),
    path('callback/', views.kakao_callback, name='callback'),  # 수정!
    # path("token/refresh/", views.token_refresh, name="token_refresh"),
    # path("logout/", views.logout, name="logout"), 
]
    # path('kakao/login/finish/', KakaoLogin.as_view(), name='login_to_django'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # #path("callback/", TemplateView.as_view(template_name="auth/callback.html")),
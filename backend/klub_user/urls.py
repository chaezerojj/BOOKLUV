from django.urls import path
from . import views
from django.views.generic import TemplateView
# from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = 'klub_user'

urlpatterns = [
    path('', views.login, name='login'),
    path('callback/', views.kakao_callback, name='callback'),  # 수정!
    path("me/", views.me, name="me"),
    path("logout/", views.logout_view, name="logout"),
]
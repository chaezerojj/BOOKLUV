from django.urls import path
from . import views

app_name = 'klub_user'

urlpatterns = [
    path('', views.login, name='login'),
    path('callback/', views.kakao_callback, name='callback'),  # 수정!
]

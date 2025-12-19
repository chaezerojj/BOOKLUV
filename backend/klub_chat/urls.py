from django.urls import path
from . import views

app_name = 'chat'  # ← 이 부분이 중요! namespace 설정

urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('<str:room_name>/', views.room_detail, name='room_detail'),
]

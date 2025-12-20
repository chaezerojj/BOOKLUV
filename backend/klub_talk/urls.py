from django.urls import path
from . import views

app_name = 'talk'

urlpatterns = [
    path('', views.aladin_api, name='book_list'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),  
    path('room/<int:pk>/', views.room_detail, name='room_detail'),
    path('quiz/<int:meeting_id>/', views.quiz_view, name='quiz'),
    
]

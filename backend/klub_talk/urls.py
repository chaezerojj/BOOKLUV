from django.urls import path
from . import views

# 책, 모임, 퀴즈 관련 앱
app_name = 'klub_talk'

urlpatterns = [
    # 도서 - 알라딘 api 데이터 기반 도서 목록
    path('', views.aladin_api, name='book_list'),
    # 책 검색
    path('books/', views.book_search_api, name="book_search_api"),
    # 도서 - 도서 상세 정보 및 관련 모임 목록
    path('books/<int:book_id>/', views.book_detail_api, name='book_detail_api'),  
    # 모임 - 해당 도서 모임 상세 페이지
    path('room/<int:pk>/', views.meeting_detail_api, name='meeting_detail_api'),
    # 퀴즈 - 모임 참여 신청 페이지 (GET, POST)
    path('quiz/<int:meeting_id>/', views.quiz_api, name='quiz_api'),
    
    path('books/page/', views.book_list, name='search_book_page'),
]

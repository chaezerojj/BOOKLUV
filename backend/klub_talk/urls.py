from django.urls import path
from . import views

app_name = 'klub_talk'

urlpatterns = [
    # 채영언니가 쓴 api
    path('', views.book_search_api, name="book-search-api"), 
    path('page/', views.book_list, name='search-book-page'),
    # 모임 상세 페이지
    path('<int:book_id>/', views.book_detail, name='book-detail'),  # GET: 단일 도서 정보, PUT/PATCH: 수정, DELETE: 삭제

    # 모임 관련
    path('rooms/<int:pk>/', views.room_detail, name='room-detail'), # GET: 모임 상세, PUT/PATCH: 수정, DELETE: 삭제

    # 퀴즈 관련
    path('meetings/<int:meeting_id>/quiz/', views.quiz_view, name='quiz-detail'),  # GET: 퀴즈 조회, POST: 참여 신청
]

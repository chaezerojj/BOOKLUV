from django.urls import path
from . import views

app_name = 'talk'

urlpatterns = [
    # 도서 - 알라딘 api 데이터 기반 도서 목록
    path('aladin/', views.aladin_api, name='aladin-books'),
    # 채영언니가 쓴 api
    # path('index', views.show_index, name="index"), 
    path('', views.book_search_api, name="book-search-api"), 
    path('page/', views.book_list, name='search-book-page'),
    # 모임 상세 페이지
    path('<int:book_id>/', views.book_detail, name='book-detail'),  # GET: 단일 도서 정보, PUT/PATCH: 수정, DELETE: 삭제
    # 모임 관련
    path('meetings/<int:pk>/', views.meeting_detail_api, name='meeting-detail'), # GET: 모임 상세, PUT/PATCH: 수정, DELETE: 삭제
    # 퀴즈 관련
    path('meetings/<int:meeting_id>/quiz/', views.quiz_view, name='quiz-detail'),  # GET: 퀴즈 조회, POST: 참여 신청,
    # 모임 검색
    path("meetings/", views.meeting_search, name="meeting-search"),
    # 모임 상세 render - 백엔드에서 확인용
    path("meetings/render/<int:pk>/", views.room_detail, name="meeting-test-detail"),
    path('<int:pk>/meeting/', views.create_meeting, name='create-meeting'),
    path('meetings/<int:meeting_id>/cancel/', views.cancel_participation, name='cancel-participation'),
    path('meetings/edit/<int:pk>/', views.edit_meeting, name='edit-meeting'),
    path('meetings/delete/<int:pk>/', views.delete_meeting, name='delete-meeting'),
]

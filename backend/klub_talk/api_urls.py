# klub_talk/api_urls.py
from django.urls import path
from . import api_views

app_name = "books_api"

urlpatterns = [
    # books
    path("", api_views.book_search_api, name="book-search"),
    path("<int:book_id>/", api_views.book_detail_api, name="book-detail"),

    # meetings
    path("meetings/", api_views.meeting_list_api, name="meeting-list"),
    path("meetings/<int:pk>/", api_views.meeting_detail_api, name="meeting-detail"),
    path("meetings/<int:pk>/quiz/", api_views.meeting_quiz_api, name="meeting-quiz"),
    path("books/meetings/<int:pk>/quiz/", api_views.meeting_quiz_api),
]
# klub_talk/api_urls.py
from django.urls import path
from . import api_views

app_name = "books_api"

urlpatterns = [
    path("", api_views.book_search_api, name="book-search"),
    path("meetings/", api_views.meeting_search_api, name="meeting-search"), 
    path("<int:book_id>/", api_views.book_detail_api, name="book-detail"),
]

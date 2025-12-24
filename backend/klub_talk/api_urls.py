from django.urls import path
from . import api_views

app_name = "books_api"

urlpatterns = [
    path("", api_views.book_search_api, name="book-search"),
    path("<int:book_id>/", api_views.book_detail_api, name="book-detail"),
]

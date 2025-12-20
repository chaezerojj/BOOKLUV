from django.urls import path
from . import views

app_name = "klub_talk"

urlpatterns = [
    path('', views.aladin_api, name="books"),
    path('books/', views.book_search_api, name="book_search_api"),
    path('books/page/', views.book_list, name='search_book_page'),
]

from django.db import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from .models import Meeting, Book
from django.db.models import Q

def index(request):
    return render(request, 'talk/index.html')

# 알라딘 api 테스트
def aladin_api(request):
    books = Book.objects.all()
    return render(request, 'talk/book_list.html', {'books': books})

def book_list(request):
    search_query = request.GET.get('q', '')  # 검색어
    type_filter = request.GET.get('type', 'book')  # 검색 타입, 기본값은 'book'

    books = Book.objects.all()  # 기본값으로 모든 책을 가져옵니다.

    if search_query:
        # 책 제목, 작가명, 장르명, 설명으로 검색
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author_id__name__icontains=search_query) |
            Q(category_id__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    return render(request, 'talk/book_list.html', {'books': books, 'type_filter': type_filter})
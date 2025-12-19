from django.db import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from .models import Meeting, Book
def index(request):
    return render(request, 'talk/index.html')

# 알라딘 api 테스트
def aladin_api(request):
    books = Book.objects.all()
    return render(request, 'talk/book_list.html', {'books': books})

def meeting_list():
    pass
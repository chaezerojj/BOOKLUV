from django.db import models
from klub_user.models import User

class Category(models.Model):
    name = models.CharField(max_length=20)
class Author(models.Model):
    name = models.CharField(max_length=20)
class Book(models.Model):
    aladin_id = models.CharField(max_length=50, unique=True) 
    title = models.CharField(max_length=255)
    author_id = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    pub_date = models.DateField(null=True, blank=True)
    cover_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    
class Meeting(models.Model):
    leader_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete = models.CASCADE)
    title = models.CharField(max_length=50, default="함께 책 읽고 소통해요")
    description = models.TextField(blank=True, default="책을 읽고 함께 이야기를 나눌 분들을 찾습니다.")
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(auto_now=True)
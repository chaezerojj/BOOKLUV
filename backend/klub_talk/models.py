from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    aladin_id = models.CharField(max_length=50, unique=True) 
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    pub_date = models.DateField(null=True, blank=True)
    cover_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    
class Meeting(models.Model):
    leader_id = models.ForeignKey(User, on_delete = models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(auto_now=True)
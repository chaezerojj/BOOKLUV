from django.db import models
from klub_user.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# 도서 장르 분류 정보
class Category(models.Model):
    name = models.CharField(max_length=20)

# 도서 작가 정보
class Author(models.Model):
    name = models.CharField(max_length=20)

# 도서 정보
class Book(models.Model):
    aladin_id = models.CharField(max_length=50, unique=True) 
    title = models.CharField(max_length=255)
    author_id = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    pub_date = models.DateField(null=True, blank=True)
    cover_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    
# 모임 정보
class Meeting(models.Model):
    leader_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete = models.CASCADE)
    title = models.CharField(max_length=50, default="함께 책 읽고 소통해요")
    description = models.TextField(blank=True, default="책을 읽고 함께 이야기를 나눌 분들을 찾습니다.")
    members = models.IntegerField(validators=
                                  # 최소 인원 2명
                                  [MinValueValidator(2),
                                   # 최대 인원 10명
                                   MaxValueValidator(10)]
                                  )
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(auto_now=True)
    
# 모임 - 퀴즈 정보
class Quiz(models.Model):
    meeting_id = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    question = models.CharField(max_length=50, default="절창의 남자 주인공 이름은?")
    answer = models.CharField(max_length=50, default="오언")

# 모임 참가 신청 정보
class Participate(models.Model):
    meeting_id = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # False = 퀴즈 틀림 True = 퀴즈 맞춤
    result = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
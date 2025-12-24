from django.db import models
from klub_user.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ValidationError

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
    
    def __str__(self):
        return self.title
    
    @property
    def author_name(self):
        return self.author_id.name if self.author_id else "정보 없음"
    
# 모임 정보

class Meeting(models.Model):
    leader_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, default="함께 책 읽고 소통해요")
    description = models.TextField(
        blank=True, 
        default="책을 읽고 함께 이야기를 나눌 분들을 찾습니다.",
        validators=[MaxLengthValidator(200)]  # 최대 200자
    )
    members = models.IntegerField(validators=[
        MinValueValidator(2),  # 최소 인원 2명
        MaxValueValidator(10)   # 최대 인원 10명
    ])
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()

    @property
    def has_started(self):
        return timezone.now() >= self.started_at
    
    @property
    def has_finished(self):
        return timezone.now() > self.finished_at

    def clean(self):
        if self.started_at and self.finished_at and self.started_at > self.finished_at:
            raise ValidationError("시작 시간은 종료 시간보다 늦을 수 없습니다.")
        
        if self.started_at and self.started_at < timezone.now():
            raise ValidationError("시작 시간은 현재 시간 이후여야 합니다.")

    def __str__(self):
        return self.title


class Quiz(models.Model):
    meeting_id = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    question = models.CharField(max_length=50, blank=True, null=True)
    answer = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Quiz for {self.meeting_id.title}"

# 모임 참가 신청 정보
class Participate(models.Model):
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name="participations"
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    result = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

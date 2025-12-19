# klub_recommend/models.py
from django.db import models
from django.contrib.auth import get_user_model
from klub_talk.models import Book
from klub_user.models import User

class ReadingPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 퀴즈 핵심 요약 필드
    purpose = models.CharField(max_length=30)          # 재미 / 사유 / 실용 / 위로
    new_vs_classic = models.CharField(max_length=20)   # 신간 / 고전 / 무관
    category = models.CharField(max_length=30)         # 인문학 / 소설 등
    mood = models.CharField(max_length=30)             # 따뜻 / 묵직 / 가벼움
    reading_style = models.CharField(max_length=30)    # 몰입 / 분할 / 선택
    length_pref = models.CharField(max_length=20)      # 짧음 / 보통 / 길어도
    difficulty_pref = models.CharField(max_length=20)  # 쉬움 / 중간 / 어려움

    created_at = models.DateTimeField(auto_now_add=True)


class RecommendationResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preference = models.ForeignKey(ReadingPreference, on_delete=models.CASCADE)

    books = models.ManyToManyField(Book)
    ai_reason = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

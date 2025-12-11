from django.db import models

class User(models.Model):
    nickname = models.CharField(max_length=20, unique=True)
    uid = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)  # 해시 저장용
    email = models.EmailField(default="example@example.com")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.nickname

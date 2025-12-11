from django.db import models

class User(models.Model):
    nickname = models.CharField(max_length=20, unique=True)
    uid = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)  # 해시 저장용
    email = models.EmailField(default="example@example.com")
    created_at = models.DateTimeField(auto_now_add=True)
    # status = 회원 상태 / 0 = 가입 중 / 1 = 탈퇴 
    status = models.IntegerField(default = 0)
    def __str__(self):
        return self.nickname

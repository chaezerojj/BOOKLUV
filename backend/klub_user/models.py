from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# 관리자 계정
class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    # 카카오톡 로그인 시 저장되는 정보
    # 이메일
    email = models.EmailField(unique=True, null=True, blank=True)
    # kakao id
    kakao_id = models.BigIntegerField(unique=True, null=True, blank=True)
    # is active
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    # 지웠을때 어떻게 될 지 모름 -> 나중에 수정~
    # objects = UserManager()

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []
    last_login = models.DateTimeField(null=True, blank=True)  # ✅ 추가


    def __str__(self):
        return self.email or f"kakao_{self.kakao_id}"
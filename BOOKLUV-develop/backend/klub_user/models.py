# # from django.db import models

# # class User(models.Model):
# #     nickname = models.CharField(max_length=20, unique=True)
# #     uid = models.CharField(max_length=30, unique=True)
# #     password = models.CharField(max_length=128)  # 해시 저장용
# #     email = models.EmailField(default="example@example.com")
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     # status = 회원 상태 / 0 = 가입 중 / 1 = 탈퇴 
# #     status = models.IntegerField(default = 0)
# #     def __str__(self):
# #         return self.nickname


# # models.py
# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class User(AbstractUser):
#     kakao_id = models.BigIntegerField(null=True, blank=True, unique=True)

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

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
    email = models.EmailField(unique=True, null=True, blank=True)
    kakao_id = models.BigIntegerField(unique=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email or f"kakao_{self.kakao_id}"


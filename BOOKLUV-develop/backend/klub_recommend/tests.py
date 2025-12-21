from django.test import TestCase
from klub_user.models import User

# 유저 테스트
def check_user():
    user = User.objects.filter(pk=1).first()
    print(user)

check_user()
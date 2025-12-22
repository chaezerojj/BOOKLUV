from django.contrib import admin

# Register your models here.
from .models import Board

# admin site에 등록
admin.site.register(Board)

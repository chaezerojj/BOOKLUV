# klub_recommend/urls.py
from django.urls import path
from . import views

app_name = "klub_recommend"

urlpatterns = [
    path("", views.quiz_view, name="quiz"),
    path("result/", views.result_view, name="result"),
]

from django.urls import path
from . import views

app_name = "recommend"

urlpatterns = [
    # 퀴즈 조회 및 참여
    # path("", views.quiz_view, name="quiz-detail"),
    path("result/", views.result_api_view, name="quiz-result"),
    # 프론드용 api
    path("api/result/", views.result_api_view, name="quiz-result-api"),
]

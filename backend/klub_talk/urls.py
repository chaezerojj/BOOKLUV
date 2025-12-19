from django.urls import path
from . import views

app_name = "klub_talk"

urlpatterns = [
    path('', views.aladin_api, name="books"),
    path('meetings', views.meeting_list, name="meetings")
]

from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("rooms/", views.room_list, name="room-list"),
    path("rooms/<slug:room_name>/", views.room_detail, name="room-detail"),  # int → slug
]
from django.urls import path
from . import api_views

app_name = "board"

urlpatterns = [
    path("", api_views.board_list_create, name="list-create"),
    path("<int:pk>/", api_views.board_detail_update_delete, name="detail-update-delete"),

    path("<int:pk>/comments/", api_views.comment_list_create, name="comment-list-create"),
    path("<int:board_pk>/comments/<int:comment_pk>/", api_views.comment_update_delete, name="comment-update-delete"),
]

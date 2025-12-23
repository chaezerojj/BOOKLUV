from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Board, Comment

User = get_user_model()


class UserMiniSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    kakao_id = serializers.SerializerMethodField()
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "kakao_id", "display_name")

    def get_email(self, obj):
        return getattr(obj, "email", None)

    def get_kakao_id(self, obj):
        return getattr(obj, "kakao_id", None)

    def get_display_name(self, obj):
        return (
            getattr(obj, "nickname", None)
            or getattr(obj, "username", None)
            or getattr(obj, "email", None)
            or f"user-{obj.id}"
        )


class CommentSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "board", "user", "content", "created_at", "updated_at")
        read_only_fields = ("id", "board", "user", "created_at", "updated_at")


class BoardListSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = ("id", "user", "title", "content", "created_at", "updated_at", "comment_count")


class BoardDetailSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(read_only=True)
    comments = CommentSerializer(source="comment_set", many=True, read_only=True)

    class Meta:
        model = Board
        fields = ("id", "user", "title", "content", "created_at", "updated_at", "comments")
        read_only_fields = ("id", "user", "created_at", "updated_at")


class BoardCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ("title", "content")

from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from .models import Board, Comment
from .serializers import (
    BoardListSerializer,
    BoardDetailSerializer,
    BoardCreateUpdateSerializer,
    CommentSerializer,
)


def _is_owner(user, obj):
    return user.is_authenticated and obj.user_id == user.id


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def board_list_create(request):
    if request.method == "GET":
        qs = (
            Board.objects.select_related("user")
            .annotate(comment_count=Count("comment", distinct=True))
            .order_by("-created_at")
        )
        return Response(BoardListSerializer(qs, many=True).data)

    # 비로그인 방지 (401)
    if not request.user.is_authenticated:
        return Response({"detail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = BoardCreateUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    board = serializer.save(user=request.user)
    return Response(BoardDetailSerializer(board).data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def board_detail_update_delete(request, pk):
    board = get_object_or_404(Board.objects.select_related("user"), pk=pk)

    if request.method == "GET":
        return Response(BoardDetailSerializer(board).data)

    if not _is_owner(request.user, board):
        return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "PATCH":
        serializer = BoardCreateUpdateSerializer(board, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        board.refresh_from_db()
        return Response(BoardDetailSerializer(board).data)

    # DELETE
    board.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_list_create(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == "GET":
        qs = Comment.objects.select_related("user").filter(board=board).order_by("created_at")
        return Response(CommentSerializer(qs, many=True).data)

    # 비로그인 방지 (401)
    if not request.user.is_authenticated:
        return Response({"detail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = CommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    comment = serializer.save(board=board, user=request.user)
    return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def comment_update_delete(request, board_pk, comment_pk):
    comment = get_object_or_404(Comment.objects.select_related("user"), pk=comment_pk, board_id=board_pk)

    if not _is_owner(request.user, comment):
        return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "PATCH":
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CommentSerializer(comment).data)

    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

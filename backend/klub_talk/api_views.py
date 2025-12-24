# klub_talk/api_views.py
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book, Meeting
from .serializers import BookSerializer


@api_view(["GET"])
def book_search_api(request):
    q = (request.GET.get("q") or "").strip()
    qs = Book.objects.all()

    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(author_id__name__icontains=q) |
            Q(category_id__name__icontains=q) |
            Q(description__icontains=q)
        )

    return Response(BookSerializer(qs, many=True).data)


@api_view(["GET"])
def book_detail_api(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    meetings_qs = (
        Meeting.objects
        .filter(book_id=book_id)
        .select_related("book_id", "leader_id")
        .order_by("-id")
    )

    meetings = []
    for m in meetings_qs:
        meetings.append({
            "id": m.id,
            "title": m.title,
            "description": getattr(m, "description", ""),
            "views": getattr(m, "views", 0),
        })

    return Response({
        "book": BookSerializer(book).data,
        "meetings": meetings,
    })


@api_view(["GET"])
def meeting_search_api(request):
    """
    프론트 전역검색(kluvtalk)용 API
    GET /api/v1/books/meetings/?q=검색어
    - 종료되지 않은 모임(finished_at > now)만 노출
    - 모임 제목 or 책 제목으로 검색
    """
    q = (request.GET.get("q") or "").strip()
    now = timezone.now()

    qs = (
        Meeting.objects
        .filter(finished_at__gt=now)
        .select_related("book_id", "book_id__category_id", "leader_id")
        .annotate(
            joined_count=Count("participations", filter=Q(participations__result=True))
        )
        .order_by("started_at")
    )

    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(book_id__title__icontains=q)
        )

    def leader_name(u):
        # 프로젝트 유저 필드 상황에 맞춰 안전하게
        return getattr(u, "nickname", None) or getattr(u, "username", None) or getattr(u, "email", None) or "Unknown"

    data = []
    for m in qs[:50]:  # 과도한 응답 방지(필요하면 조절)
        data.append({
            "id": m.id,
            "title": m.title,
            "description": getattr(m, "description", ""),
            "host_name": leader_name(m.leader_id) if m.leader_id else None,
            "category_name": getattr(getattr(m.book_id, "category_id", None), "name", None),
            "book_title": getattr(m.book_id, "title", None),
            "book_id": getattr(m.book_id, "id", None),
            "book_cover_url": getattr(m.book_id, "cover_url", None),

            "started_at": getattr(m, "started_at", None),
            "finished_at": getattr(m, "finished_at", None),
            "joined_count": getattr(m, "joined_count", 0),
            "views": getattr(m, "views", 0),
        })

    return Response(data)

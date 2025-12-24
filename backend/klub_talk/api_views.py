# klub_talk/api_views.py
from django.db.models import Q, Count
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Book, Meeting, Participate, Quiz
from .serializers import BookSerializer
from .serializers import QuizSerializer


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

def serialize_meeting(m, joined_count=None):
    return {
        "id": m.id,
        "title": m.title,
        "description": getattr(m, "description", "") or "",
        "views": getattr(m, "views", 0) or 0,

        # 정원/멤버 필드가 프로젝트마다 달라서 방어적으로
        "members": getattr(m, "members", None) or getattr(m, "max_members", None) or 0,
        "joined_count": joined_count if joined_count is not None else None,

        "started_at": m.started_at.isoformat() if getattr(m, "started_at", None) else None,
        "finished_at": m.finished_at.isoformat() if getattr(m, "finished_at", None) else None,

        "book_id": getattr(m.book_id, "id", None) if getattr(m, "book_id", None) else None,
        "book_title": getattr(m.book_id, "title", None) if getattr(m, "book_id", None) else None,

        "leader_id": getattr(m.leader_id, "id", None) if getattr(m, "leader_id", None) else None,
        "leader_name": getattr(m.leader_id, "nickname", None) if getattr(m, "leader_id", None) else None,
        "host_name": getattr(m.leader_id, "nickname", None) if getattr(m, "leader_id", None) else None,

        "category_name": getattr(getattr(m.book_id, "category_id", None), "name", None),
    }
    
@api_view(["GET"])
def meeting_list_api(request):
    """
    GET /api/v1/books/meetings/?q=...&sort=views|soon&limit=10
    - q: 모임 제목/책 제목 검색
    - sort=views : 조회수 높은 순
    - sort=soon  : 시작 임박 순(기본)
    """
    q = (request.GET.get("q") or "").strip()
    sort = (request.GET.get("sort") or "soon").strip()
    limit = request.GET.get("limit")

    now = timezone.localtime()

    qs = (
        Meeting.objects
        .select_related("book_id", "book_id__category_id", "leader_id")
        .filter(finished_at__gt=now)  # 종료 안된 모임(진행중/예정)만
        .annotate(
            joined_count=Count(
                "participations",
                filter=Q(participations__result=True)
            )
        )
    )

    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(book_id__title__icontains=q)
        )

    if sort == "views":
        qs = qs.order_by("-views", "-id")
    else:
        qs = qs.order_by("started_at", "-id")

    if limit:
        try:
            qs = qs[: int(limit)]
        except ValueError:
            pass

    data = [serialize_meeting(m, joined_count=getattr(m, "joined_count", None)) for m in qs]
    return Response(data, status=status.HTTP_200_OK)


@api_view(["GET"])
def meeting_detail_api(request, pk):
    """
    GET /api/v1/books/meetings/<id>/
    """
    meeting = get_object_or_404(
        Meeting.objects.select_related("book_id", "book_id__category_id", "leader_id"),
        pk=pk
    )

    joined_count = Participate.objects.filter(meeting=meeting, result=True).count()

    return Response({
        **serialize_meeting(meeting, joined_count=joined_count),
        # 필요하면 추가 필드 더 넣어도 됨
    }, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def meeting_quiz_api(request, pk):
    """
    GET  /api/v1/books/meetings/<id>/quiz/
    POST /api/v1/books/meetings/<id>/quiz/  {answer: "..."}
    """
    quiz = get_object_or_404(Quiz, meeting_id=pk)

    if request.method == "GET":
        return Response(QuizSerializer(quiz).data, status=status.HTTP_200_OK)

    user_answer = (request.data.get("answer") or "").strip()
    correct = (quiz.answer or "").strip()
    result = (user_answer == correct)

    return Response({
        "question": quiz.question,
        "user_answer": user_answer,
        "answer": correct,
        "result": result,
    }, status=status.HTTP_200_OK)
# klub_talk/api_views.py
from django.db.models import Q, Count
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Book, Meeting, Participate, Quiz
from .serializers import BookSerializer, QuizSerializer

MAX_ATTEMPTS = 3

# =========================
# 유틸리티 함수
# =========================

def normalize_answer(s: str) -> str:
    if s is None:
        return ""
    s = str(s).strip().replace(" ", "")
    if s.endswith("년"):
        s = s[:-1]
    return s

def _parse_dt(value):
    if not value:
        return None
    from django.utils.dateparse import parse_datetime
    from django.utils import timezone
    try:
        dt = parse_datetime(value)
        if not dt:
            return None
        if timezone.is_naive(dt):
            return timezone.make_aware(dt)
        return dt
    except Exception:
        return None

def serialize_meeting(m, joined_count=None):
    """Meeting 객체를 프론트엔드용 딕셔너리로 변환"""
    book_obj = None
    if getattr(m, "book_id", None):
        book_obj = {
            "id": m.book_id.id,
            "title": m.book_id.title,
            "cover_url": getattr(m.book_id, "cover_url", None),
        }

    return {
        "id": m.id,
        "title": m.title,
        "description": getattr(m, "description", "") or "",
        "views": getattr(m, "views", 0),
        "members": getattr(m, "members", 0),
        "joined_count": joined_count,
        "started_at": m.started_at.isoformat() if m.started_at else None,
        "finished_at": m.finished_at.isoformat() if m.finished_at else None,
        "book": book_obj,
        "leader_name": getattr(m.leader_id, "nickname", "익명") if m.leader_id else "Unknown",
        "host_name": getattr(m.leader_id, "nickname", "익명") if m.leader_id else "Unknown",
        "category_name": getattr(m.book_id.category_id, "name", None) if m.book_id and getattr(m.book_id, "category_id", None) else None,
    }

# =========================
# API 뷰 함수
# =========================

@api_view(["GET"])
def book_search_api(request):
    q = (request.GET.get("q") or "").strip()
    qs = Book.objects.all()
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(author_id__name__icontains=q) |
            Q(category_id__name__icontains=q)
        )
    return Response(BookSerializer(qs, many=True).data)

@api_view(["GET"])
def book_detail_api(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    now = timezone.now()
    meetings_qs = Meeting.objects.filter(
        book_id=book_id,
        finished_at__gt=now
    ).select_related("leader_id").order_by("-id")

    meetings = [serialize_meeting(m) for m in meetings_qs]
    return Response({
        "book": BookSerializer(book).data,
        "meetings": meetings,
    })
    
    
@api_view(["GET", "POST"])
def meeting_list_api(request):
    """
    GET: 모임 목록 조회
    POST: 새로운 모임 생성
    """

    def _force_aware(value):
        """
        프론트엔드에서 넘어온 Naive 시간(timezone 정보 없음)을 
        Django 설정 시간대에 맞춘 Aware 상태로 강제 변환합니다.
        """
        if not value:
            return None
        
        # 1. 문자열인 경우 datetime 객체로 파싱
        dt = parse_datetime(value) if isinstance(value, str) else value
        if not dt:
            return None
            
        # 2. Naive(offset-naive)인 경우 설정된 시간대(Asia/Seoul 등)를 입힘
        if timezone.is_naive(dt):
            return timezone.make_aware(dt, timezone.get_current_timezone())
        
        # 3. 이미 Aware(offset-aware)인 경우 일관성을 위해 로컬 시간대로 변환
        return timezone.localtime(dt)

    # ---------- POST: 모임 생성 ----------
    if request.method == "POST":
        if not request.user.is_authenticated:
            return Response({"detail": "로그인이 필요합니다."}, status=401)

        payload = request.data or {}
        
        # 1. 시간 데이터 강제 Aware 변환 (여기서 비교 에러 원천 차단)
        started_at = _force_aware(payload.get("started_at"))
        finished_at = _force_aware(payload.get("finished_at"))
        now = timezone.now() # Django 설정에 따라 항상 Aware임

        # 2. 필수 값 및 유효성 체크
        if not (started_at and finished_at):
            return Response({"detail": "시간 정보가 누락되었거나 형식이 잘못되었습니다."}, status=400)

        # 3. 시간 비교 (둘 다 Aware이므로 에러가 발생하지 않음)
        if started_at >= finished_at:
            return Response({"detail": "시작 시간은 종료 시간보다 빨라야 합니다."}, status=400)
        
        if started_at < now:
            return Response({"detail": "과거 시간으로 모임을 생성할 수 없습니다."}, status=400)

        try:
            with transaction.atomic():
                book = get_object_or_404(Book, pk=payload.get("book_id"))
                
                # 모임 생성
                meeting = Meeting.objects.create(
                    leader_id=request.user,
                    book_id=book,
                    title=(payload.get("title") or "").strip(),
                    description=(payload.get("description") or "").strip(),
                    members=int(payload.get("members", 2)),
                    started_at=started_at,
                    finished_at=finished_at,
                )

                # 퀴즈 생성
                quiz_data = payload.get("quiz") or {}
                Quiz.objects.create(
                    meeting_id=meeting,
                    question=quiz_data.get("question") or "참여 퀴즈가 없습니다.",
                    answer=quiz_data.get("answer") or "없음"
                )

                # 리더 자동 참여
                Participate.objects.create(meeting=meeting, user_id=request.user, result=True)

                # serialize_meeting은 프로젝트 내 정의된 함수를 사용하세요
                return Response(serialize_meeting(meeting, joined_count=1), status=201)
        
        except Exception as e:
            return Response({"detail": f"저장 실패: {str(e)}"}, status=400)

    # ---------- GET: 리스트 조회 ----------
    now = timezone.now()
    sort = (request.GET.get("sort") or "soon").strip()
    limit = request.GET.get("limit")

    qs = (
        Meeting.objects
        .filter(finished_at__gt=now) # Aware vs Aware 비교
        .select_related("book_id", "leader_id")
        .annotate(joined_count=Count("participations", filter=Q(participations__result=True)))
    )

    # 검색 처리
    q = (request.GET.get("q") or "").strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(book_id__title__icontains=q))

    # 정렬 처리
    if sort == "views":
        qs = qs.order_by("-views", "-id")
    else:
        # 곧 시작하는 순서
        qs = qs.order_by("started_at", "-id")

    if limit:
        try:
            qs = qs[:int(limit)]
        except ValueError:
            pass

    data = [serialize_meeting(m, joined_count=getattr(m, 'joined_count', 0)) for m in qs]
    return Response(data)

@api_view(["GET", "PATCH", "DELETE"])
def meeting_detail_api(request, pk):
    meeting = get_object_or_404(Meeting.objects.select_related("book_id", "leader_id"), pk=pk)

    if request.method == "GET":
        joined_count = Participate.objects.filter(meeting=meeting, result=True).count()
        quiz_obj = None
        try:
            q = Quiz.objects.get(meeting_id=meeting)
            quiz_obj = {"question": q.question, "answer": q.answer}
        except Quiz.DoesNotExist:
            pass
        
        data = serialize_meeting(meeting, joined_count=joined_count)
        data["quiz"] = quiz_obj
        return Response(data)

    if not request.user.is_authenticated:
        return Response({"detail": "로그인이 필요합니다."}, status=401)

    if request.user != meeting.leader_id:
        return Response({"detail": "권한이 없습니다."}, status=403)

    if request.method == "DELETE":
        meeting.delete()
        return Response(status=204)

    if request.method == "PATCH":
        payload = request.data
        if "title" in payload: meeting.title = payload["title"]
        if "description" in payload: meeting.description = payload["description"]
        if "started_at" in payload: meeting.started_at = _parse_dt(payload["started_at"])
        if "finished_at" in payload: meeting.finished_at = _parse_dt(payload["finished_at"])
        meeting.save()
        return Response(serialize_meeting(meeting))

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def meeting_quiz_api(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    quiz = get_object_or_404(Quiz, meeting_id=meeting)

    participate_qs = Participate.objects.filter(meeting=meeting, user_id=request.user)
    already_joined = participate_qs.filter(result=True).exists()
    attempts_used = participate_qs.count()

    if request.method == "GET":
        return Response({
            "question": quiz.question,
            "attempts_used": attempts_used,
            "joined": already_joined,
            "locked": (not already_joined and attempts_used >= MAX_ATTEMPTS)
        })

    if already_joined or attempts_used >= MAX_ATTEMPTS:
        return Response({"detail": "더 이상 참여할 수 없습니다."}, status=400)

    user_answer = normalize_answer(request.data.get("answer"))
    correct_answer = normalize_answer(quiz.answer)
    is_correct = (user_answer == correct_answer)

    Participate.objects.create(meeting=meeting, user_id=request.user, result=is_correct)

    return Response({
        "result": is_correct,
        "message": "정답입니다!" if is_correct else "틀렸습니다.",
        "joined": is_correct
    })
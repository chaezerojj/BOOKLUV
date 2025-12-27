# klub_talk/api_views.py
from django.db.models import Q, Count
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Book, Meeting, Participate, Quiz
from .serializers import BookSerializer, QuizSerializer


MAX_ATTEMPTS = 3

def normalize_answer(s: str) -> str:
    # "1980" vs "1980년" 같은 차이를 줄이고 싶으면 이거 쓰면 됨
    # 필요 없으면 단순 strip만 해도 됨
    if s is None:
        return ""
    s = str(s).strip()
    s = s.replace(" ", "")
    if s.endswith("년"):
        s = s[:-1]
    return s

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
    
    # 현재 시간 기준 설정
    now = timezone.now()

    meetings_qs = (
        Meeting.objects
        .filter(
            book_id=book_id,
            started_at__gt=now,    # 아직 시작하지 않았고
            finished_at__gt=now    # 종료되지 않은 모임만
        )
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
            "started_at": m.started_at, # 시간 정보도 프론트에 주면 좋으니 추가 권장
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
    # Include book cover info so frontend can display covers (book_cover_url, and a minimal book object)
    book_obj = None
    if getattr(m, "book_id", None):
        book_obj = {
            "id": getattr(m.book_id, "id", None),
            "title": getattr(m.book_id, "title", None),
            "cover_url": getattr(m.book_id, "cover_url", None),
        }

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
        "book_cover_url": getattr(m.book_id, "cover_url", None) if getattr(m, "book_id", None) else None,
        "book": book_obj,

        "leader_id": getattr(m.leader_id, "id", None) if getattr(m, "leader_id", None) else None,
        "leader_name": getattr(m.leader_id, "nickname", None) if getattr(m, "leader_id", None) else None,
        "host_name": getattr(m.leader_id, "nickname", None) if getattr(m, "leader_id", None) else None,

        "category_name": getattr(getattr(m.book_id, "category_id", None), "name", None),
    }
    
@api_view(["GET", "POST"])
def meeting_list_api(request):
    """
    GET  /api/v1/books/meetings/?q=...&sort=views|soon&limit=10
    POST /api/v1/books/meetings/
      {
        "book_id": 1,
        "title": "...",
        "description": "...",
        "members": 5,
        "started_at": "2025-12-25T12:00:00+09:00",
        "finished_at": "2025-12-25T13:00:00+09:00",
        "quiz": { "question": "...", "answer": "..." }
      }
    """

    # ---------- POST: 생성 ----------
    if request.method == "POST":
        if not request.user or not request.user.is_authenticated:
            return Response({"detail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        payload = request.data or {}

        book_id = payload.get("book_id")
        title = (payload.get("title") or "").strip()
        description = (payload.get("description") or "").strip()
        members = payload.get("members")

        # parse datetimes (defensive)
        # 195번 라인 근처의 _parse_dt 함수를 찾아서 아래처럼 수정하세요.

    def _parse_dt(value):
        if not value:
            return None
        from django.utils.dateparse import parse_datetime
        dt = parse_datetime(value)
        if not dt:
            return None
    
        # 시간대 정보가 없는 Naive 객체라면, Django 기본 시간대를 입혀서 Aware 객체로 변환
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)
            return dt

        started_at = _parse_dt(payload.get("started_at"))
        finished_at = _parse_dt(payload.get("finished_at"))

        quiz = payload.get("quiz") or {}
        question = (quiz.get("question") or "").strip()
        answer = (quiz.get("answer") or "").strip()

        # ---- validation (최소한만) ----
        if not book_id:
            return Response({"book_id": "book_id가 필요합니다."}, status=400)
        if not title:
            return Response({"title": "모임 제목을 입력해주세요."}, status=400)
        if members is None:
            return Response({"members": "인원을 입력해주세요."}, status=400)
        try:
            members = int(members)
        except:
            return Response({"members": "인원은 숫자여야 합니다."}, status=400)

        if members < 2 or members > 10:
            return Response({"members": "인원은 2~10명이어야 합니다."}, status=400)

        if not started_at or not finished_at:
            return Response({"time": "시작/종료 시간을 입력해주세요."}, status=400)
        if started_at >= finished_at:
            return Response({"time": "시작 시간은 종료 시간보다 빨라야 합니다."}, status=400)
        if started_at < timezone.now():
            return Response({"time": "시작 시간은 현재 이후여야 합니다."}, status=400)

        if len(description) > 200:
            return Response({"description": "설명은 200자 이하여야 합니다."}, status=400)

        book = get_object_or_404(Book, pk=book_id)

        meeting = Meeting.objects.create(
            leader_id=request.user,
            book_id=book,
            title=title,
            description=description,
            members=members,
            started_at=started_at,
            finished_at=finished_at,
        )

        created_quiz = Quiz.objects.create(
            meeting_id=meeting,
            question=question if question else None,
            answer=answer if answer else None,
        )

        return Response(
            {
                **serialize_meeting(meeting, joined_count=0),
                "quiz": QuizSerializer(created_quiz).data,
            },
            status=status.HTTP_201_CREATED,
        )
    # ---------- GET: 기존 리스트 로직 ----------
    q = (request.GET.get("q") or "").strip()
    sort = (request.GET.get("sort") or "soon").strip()
    limit = request.GET.get("limit")

    # [중요] 기준이 되는 현재 시간
    now = timezone.now()

    qs = (
        Meeting.objects
        .select_related("book_id", "book_id__category_id", "leader_id")
        # 1. 종료 시간이 미래여야 함 (이미 끝난 모임 제외)
        # 2. 시작 시간도 미래여야 함 (이미 진행 중인 모임 제외 - 필요 시 선택)
        .filter(finished_at__gt=now, started_at__gt=now) 
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


from django.utils.dateparse import parse_datetime


@api_view(["GET", "PATCH", "DELETE"])
def meeting_detail_api(request, pk):
    """
    GET /api/v1/books/meetings/<id>/
    PATCH /api/v1/books/meetings/<id>/  (leader only)
    DELETE /api/v1/books/meetings/<id>/ (leader only)
    """
    meeting = get_object_or_404(
        Meeting.objects.select_related("book_id", "book_id__category_id", "leader_id"),
        pk=pk
    )

    # GET: 그대로 반환
    if request.method == "GET":
        joined_count = Participate.objects.filter(meeting=meeting, result=True).count()
        # attach quiz if exists
        quiz_obj = None
        try:
            q = Quiz.objects.get(meeting_id=meeting)
            quiz_obj = {"question": q.question, "answer": q.answer}
        except Quiz.DoesNotExist:
            quiz_obj = None

        payload = {**serialize_meeting(meeting, joined_count=joined_count)}
        if quiz_obj:
            payload["quiz"] = quiz_obj

        return Response(payload, status=status.HTTP_200_OK)

    # For PATCH / DELETE: require authentication
    if not request.user or not request.user.is_authenticated:
        return Response({"detail": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    # Only meeting leader may modify/delete
    if request.user != meeting.leader_id:
        return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    # DELETE: remove and return 204
    if request.method == "DELETE":
        meeting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PATCH: partial update
    payload = request.data or {}

    title = payload.get("title")
    description = payload.get("description")
    members = payload.get("members")
    started_at_raw = payload.get("started_at")
    finished_at_raw = payload.get("finished_at")
    quiz_payload = payload.get("quiz")

    if title is not None:
        meeting.title = (title or "").strip()
    if description is not None:
        meeting.description = (description or "").strip()
    if members is not None:
        try:
            meeting.members = int(members)
        except Exception:
            return Response({"members": "인원은 숫자여야 합니다."}, status=400)
        if meeting.members < 2 or meeting.members > 10:
            return Response({"members": "인원은 2~10명이어야 합니다."}, status=400)

    # parse datetimes if provided
    try:
        if started_at_raw is not None:
            dt = parse_datetime(started_at_raw)
            if dt is None:
                raise ValueError("invalid datetime")
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt)
            meeting.started_at = dt
        if finished_at_raw is not None:
            dt2 = parse_datetime(finished_at_raw)
            if dt2 is None:
                raise ValueError("invalid datetime")
            if timezone.is_naive(dt2):
                dt2 = timezone.make_aware(dt2)
            meeting.finished_at = dt2
    except Exception:
        return Response({"time": "시작/종료 시간 형식이 올바르지 않습니다."}, status=400)

    # validate model (clean) and save
    try:
        meeting.full_clean()
        meeting.save()
    except Exception as e:
        # 모델 검증 오류 메시지 정리
        return Response({"detail": str(e)}, status=400)

    # quiz update (optional)
    if isinstance(quiz_payload, dict):
        quiz = None
        try:
            quiz = Quiz.objects.get(meeting_id=meeting)
        except Quiz.DoesNotExist:
            quiz = None

        question = (quiz_payload.get("question") or "").strip() if quiz_payload.get("question") is not None else None
        answer = (quiz_payload.get("answer") or "").strip() if quiz_payload.get("answer") is not None else None

        if quiz:
            if question is not None:
                quiz.question = question
            if answer is not None:
                quiz.answer = answer
            quiz.save()
        else:
            # only create if any content provided
            if (question or answer):
                Quiz.objects.create(meeting_id=meeting, question=question or None, answer=answer or None)

    joined_count = Participate.objects.filter(meeting=meeting, result=True).count()
    return Response({**serialize_meeting(meeting, joined_count=joined_count)}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def meeting_quiz_api(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    quiz = get_object_or_404(Quiz, meeting_id=pk)

    already_joined = Participate.objects.filter(
        meeting=meeting,
        user_id=request.user,
        result=True
    ).exists()

    attempts_used = Participate.objects.filter(
        meeting=meeting,
        user_id=request.user
    ).count()

    attempts_left = max(0, MAX_ATTEMPTS - attempts_used)
    locked = (not already_joined) and (attempts_used >= MAX_ATTEMPTS)

    # -------- GET --------
    if request.method == "GET":
        return Response({
            "meeting_id": meeting.id,
            "question": quiz.question,
            "attempts_used": attempts_used,
            "attempts_left": attempts_left,
            "locked": locked,
            "joined": already_joined,
        }, status=status.HTTP_200_OK)

    # -------- POST --------
    if already_joined:
        return Response({
            "question": quiz.question,
            "user_answer": "",
            "result": True,
            "attempts_used": attempts_used,
            "attempts_left": attempts_left,
            "locked": False,
            "joined": True,
            "message": "이미 참여가 완료된 모임입니다.",
        }, status=status.HTTP_200_OK)

    if locked:
        return Response({
            "question": quiz.question,
            "user_answer": "",
            "result": False,
            "attempts_used": attempts_used,
            "attempts_left": 0,
            "locked": True,
            "joined": False,
            "message": "시도 횟수를 모두 소진했습니다. 참여가 불가합니다.",
        }, status=status.HTTP_200_OK)

    user_answer_raw = (request.data.get("answer") or "")
    user_answer = normalize_answer(user_answer_raw)
    correct = normalize_answer(quiz.answer or "")

    is_correct = (user_answer == correct)

    Participate.objects.create(
        meeting=meeting,
        user_id=request.user,
        result=is_correct
    )

    attempts_used += 1
    attempts_left = max(0, MAX_ATTEMPTS - attempts_used)
    locked = (not is_correct) and (attempts_left == 0)

    return Response({
        "question": quiz.question,
        "user_answer": user_answer_raw,
        "result": is_correct,

        "attempts_used": attempts_used,
        "attempts_left": attempts_left,
        "locked": locked,
        "joined": is_correct,

        "message": "정답입니다. 참여가 완료되었습니다." if is_correct else "틀렸습니다.",
    }, status=status.HTTP_200_OK)
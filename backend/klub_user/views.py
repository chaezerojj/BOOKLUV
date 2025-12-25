from datetime import timedelta

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.text import slugify
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from klub_chat.models import Room
from klub_talk.models import Participate

User = get_user_model()

KAKAO_REST_API_KEY = settings.KAKAO_REST_API_KEY
KAKAO_REDIRECT_URI = settings.KAKAO_REDIRECT_URI
KAKAO_CLIENT_SECRET = settings.KAKAO_CLIENT_SECRET


def auth_login(request):
    """
    로그인 페이지 렌더링
    - next(또는 state)에 대한 흐름을 유지하기 위해 next 값을 템플릿으로 전달
    """
    context = {
        "KAKAO_REST_API_KEY": KAKAO_REST_API_KEY,
        "KAKAO_REDIRECT_URI": KAKAO_REDIRECT_URI,
        "next": request.GET.get("next", ""),
    }
    return render(request, "auth/login.html", context)


def kakao_callback(request):
    """
    카카오 OAuth 콜백
    - code로 access_token 발급
    - /v2/user/me로 사용자 정보 조회
    - kakao_id 기준으로 유저 생성/조회
    - 세션 로그인
    - state(프론트에서 next 목적지로 사용) 있으면 그쪽으로 redirect
      없으면 FRONT_URL + "/"
    """
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"detail": "missing code"}, status=400)

    try:
        token_res = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": KAKAO_REST_API_KEY,
                "redirect_uri": KAKAO_REDIRECT_URI,
                "client_secret": KAKAO_CLIENT_SECRET,
                "code": code,
            },
            timeout=5,
        )

        if token_res.status_code != 200:
            return JsonResponse(
                {"detail": "token exchange failed", "kakao": token_res.text},
                status=400,
            )

        access_token = token_res.json().get("access_token")
        if not access_token:
            return JsonResponse(
                {"detail": "no access_token", "kakao": token_res.json()},
                status=400,
            )

        me_res = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=5,
        )

        if me_res.status_code != 200:
            return JsonResponse(
                {"detail": "user info failed", "kakao": me_res.text},
                status=400,
            )

        me = me_res.json()
        kakao_id = me.get("id")
        kakao_account = me.get("kakao_account", {})
        email = kakao_account.get("email")  # 동의 안 받으면 None

        if not kakao_id:
            return JsonResponse({"detail": "missing kakao id", "me": me}, status=400)

        # 유저 생성/조회 (kakao_id 기준)
        user, _created = User.objects.get_or_create(
            kakao_id=kakao_id,
            defaults={
                "email": email or f"kakao_{kakao_id}@kakao.local",
                "is_active": True,
            },
        )

        # 세션 로그인
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        # 프론트에서 state를 next_url로 쓴다면 여기서 처리
        next_url = request.GET.get("state")
        if next_url:
            return redirect(next_url)

        return redirect(settings.FRONT_URL + "/")

    except Exception as e:
        return JsonResponse({"detail": "callback exception", "error": repr(e)}, status=500)


# =========================
# 프론트용 API (DRF)
# =========================

@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user

    # 조회
    if request.method == "GET":
        return Response({
            "id": user.id,
            "email": getattr(user, "email", None),
            "kakao_id": getattr(user, "kakao_id", None),
            "username": getattr(user, "username", None),
            "nickname": getattr(user, "nickname", None),
            "date_joined": getattr(user, "date_joined", None),
            "is_authenticated": True,
        })

    # 수정 (PATCH)
    nickname = request.data.get("nickname", None)
    if nickname is None:
        return Response({"detail": "nickname is required"}, status=status.HTTP_400_BAD_REQUEST)

    nickname = str(nickname).strip()
    if len(nickname) == 0:
        return Response({"detail": "nickname cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

    user.nickname = nickname
    user.save(update_fields=["nickname"])

    return Response({
        "id": user.id,
        "email": getattr(user, "email", None),
        "kakao_id": getattr(user, "kakao_id", None),
        "username": getattr(user, "username", None),
        "nickname": getattr(user, "nickname", None),
        "date_joined": getattr(user, "date_joined", None),
        "is_authenticated": True,
    })


@api_view(["POST"])
def logout_view(request):
    """
    세션 로그아웃
    POST /api/v1/auth/logout/
    """
    logout(request)
    return Response({"detail": "logged out"})


# =========================
# 기존 템플릿 페이지들
# =========================

@login_required(login_url="/api/v1/auth/")
def mypage(request):
    return render(request, "auth/mypage.html", {"user": request.user})


@login_required(login_url="/api/v1/auth/")
def mypage_edit(request):
    user = request.user

    if request.method == "POST":
        nickname = request.POST.get("nickname")
        if nickname:
            user.nickname = nickname
            user.save()
        return redirect("user:mypage")

    return render(request, "klub_user/mypage_edit.html")


@login_required(login_url="/api/v1/auth/")
def myroom(request):
    participations = (
        Participate.objects
        .filter(user_id=request.user)
        .select_related("meeting_id", "meeting_id__room")
    )

    room_infos = []
    now = timezone.localtime()

    for p in participations:
        meeting = p.meeting_id
        if not meeting:
            continue

        room = getattr(meeting, "room", None)
        if not room:
            continue

        # ✅ started_at/finished_at NULL 안전 처리
        if not meeting.started_at or not meeting.finished_at:
            is_active = False
        else:
            is_active = meeting.started_at <= now <= meeting.finished_at

        room_infos.append(
            {
                "room_name": room.name,
                "started_at": meeting.started_at,
                "finished_at": meeting.finished_at,
                "is_active": is_active,
            }
        )

    return render(request, "auth/myroom.html", {"room_infos": room_infos})


@api_view(["GET"])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def csrf(request):
    # csrftoken 쿠키를 심고, 토큰 값을 body로도 내려줌
    return Response({"csrfToken": get_token(request)})


# =========================
# ✅ 마이페이지 "나의 채팅방" JSON API
# - 진행예정 / 진행전(10분 이내) / 진행중 분류
# - 시작 10분 전~종료 전이면 Room 자동 생성
# - ✅ Participate에 result 필드가 없어도 500 안 나게 (result 필터 제거)
# - ✅ started_at/finished_at NULL 안전 처리
# =========================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def myroom_api(request):
    user = request.user
    now = timezone.localtime()

    participations = (
        Participate.objects
        .filter(user_id=user)  # ✅ result=True 제거
        .select_related("meeting_id", "meeting_id__room")
        .order_by("meeting_id__started_at")
    )

    # 1) 시작 10분 전~종료 전 구간이면 room 자동 생성(시작/종료 시간이 있을 때만)
    ten_minutes_later = now + timedelta(minutes=10)
    meetings_to_create = []

    for p in participations:
        m = p.meeting_id
        if not m or not m.started_at or not m.finished_at:
            continue

        should_have_room = (m.started_at <= ten_minutes_later and m.finished_at >= now)
        has_room = getattr(m, "room", None) is not None

        if should_have_room and not has_room:
            meetings_to_create.append(m)

    if meetings_to_create:
        with transaction.atomic():
            for m in meetings_to_create:
                safe_title = m.title or "meeting"
                new_slug = f"{slugify(safe_title)}-{m.id}"

                Room.objects.get_or_create(
                    meeting=m,
                    defaults={"name": safe_title, "slug": new_slug},
                )

    # 2) room 생성 반영 위해 재조회
    participations = (
        Participate.objects
        .filter(user_id=user)
        .select_related("meeting_id", "meeting_id__room")
        .order_by("meeting_id__started_at")
    )

    def calc_status(m):
        # 시간이 없으면 일단 예정 처리
        if not m.started_at or not m.finished_at:
            return "진행예정"

        open_at = m.started_at - timedelta(minutes=10)

        if now < open_at:
            return "진행예정"
        if open_at <= now < m.started_at:
            return "진행전"
        if m.started_at <= now <= m.finished_at:
            return "진행중"
        return "종료"

    def _safe_iso(dt):
        if not dt:
            return None
        try:
            return timezone.localtime(dt).isoformat()
        except Exception:
            try:
                # timezone-naive fallback
                aware = timezone.make_aware(dt, timezone.get_default_timezone())
                return timezone.localtime(aware).isoformat()
            except Exception:
                return dt.isoformat()

    results = []
    for p in participations:
        m = p.meeting_id
        if not m:
            continue

        status_label = calc_status(m)
        if status_label == "종료":
            continue  # 종료도 보여주려면 삭제

        room = getattr(m, "room", None)
        room_slug = getattr(room, "slug", None) if room else None

        results.append({
            "meeting_id": m.id,
            "title": m.title,
            "started_at": _safe_iso(m.started_at),
            "finished_at": _safe_iso(m.finished_at),
            "status": status_label,

            "room_slug": room_slug,
            "can_enter": (room is not None and status_label in ["진행전", "진행중"]),
            "can_chat": (status_label == "진행중"),
        })

    return Response({"results": results}, status=status.HTTP_200_OK)

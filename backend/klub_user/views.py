from datetime import timedelta

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from klub_talk.models import Participate

User = get_user_model()

KAKAO_REST_API_KEY = settings.KAKAO_REST_API_KEY
KAKAO_REDIRECT_URI = settings.KAKAO_REDIRECT_URI
KAKAO_CLIENT_SECRET = settings.KAKAO_CLIENT_SECRET

# =========================
# 유틸리티 및 인증 클래스
# =========================

class UnsafeSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # CSRF 검사 패스

# =========================
# 카카오 로그인 관련
# =========================

def auth_login(request):
    context = {
        "KAKAO_REST_API_KEY": KAKAO_REST_API_KEY,
        "KAKAO_REDIRECT_URI": KAKAO_REDIRECT_URI,
        "next": request.GET.get("next", ""),
    }
    return render(request, "auth/login.html", context)


def kakao_callback(request):
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
            return JsonResponse({"detail": "token exchange failed", "kakao": token_res.text}, status=400)

        access_token = token_res.json().get("access_token")
        me_res = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=5,
        )

        me = me_res.json()
        kakao_id = me.get("id")
        kakao_account = me.get("kakao_account", {})
        email = kakao_account.get("email")

        user, _created = User.objects.get_or_create(
            kakao_id=kakao_id,
            defaults={
                "email": email or f"kakao_{kakao_id}@kakao.local",
                "is_active": True,
            },
        )

        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        next_url = request.GET.get("state")
        return redirect(next_url) if next_url else redirect(settings.FRONT_URL + "/")

    except Exception as e:
        return JsonResponse({"detail": "callback exception", "error": repr(e)}, status=500)


# =========================
# 유저 정보 API
# =========================

@api_view(["GET", "PATCH"])
@authentication_classes([UnsafeSessionAuthentication])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    if request.method == "GET":
        return Response({
            "id": user.id,
            "email": getattr(user, "email", None),
            "nickname": getattr(user, "nickname", None),
            "is_authenticated": True,
        })

    nickname = request.data.get("nickname", "").strip()
    if not nickname:
        return Response({"detail": "nickname is required"}, status=400)

    user.nickname = nickname
    user.save(update_fields=["nickname"])
    return Response({"id": user.id, "nickname": user.nickname, "is_authenticated": True})


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"detail": "logged out"})


# =========================
# 기존 템플릿 뷰 (수정 완료)
# =========================

@login_required(login_url="/api/v1/auth/")
def mypage(request):
    return render(request, "auth/mypage.html", {"user": request.user})


@login_required(login_url="/api/v1/auth/")
def myroom(request):
    participations = (
        Participate.objects
        .filter(user_id=request.user)
        .select_related("meeting_id", "meeting_id__room")
    )

    room_infos = []
    seen_meeting_ids = set()
    # [수정] naive datetime 에러 방지
    now = timezone.now()

    for p in participations:
        meeting = p.meeting_id
        if not meeting: continue
        room = getattr(meeting, "room", None)
        if not room: continue

        # [수정] DB의 aware 시간과 now() 비교
        is_active = False
        if meeting.started_at and meeting.finished_at:
            is_active = meeting.started_at <= now <= meeting.finished_at

        room_infos.append({
            "room_name": room.name,
            "started_at": meeting.started_at,
            "finished_at": meeting.finished_at,
            "is_active": is_active,
        })
        seen_meeting_ids.add(meeting.id)

    # 리더인 모임 추가
    try:
        from klub_talk.models import Meeting
        leader_meetings = Meeting.objects.filter(leader_id=request.user).select_related("room")
        for m in leader_meetings:
            if m.id in seen_meeting_ids: continue
            room = getattr(m, "room", None)
            if not room: continue
            
            is_active = (m.started_at <= now <= m.finished_at) if (m.started_at and m.finished_at) else False
            room_infos.append({
                "room_name": room.name,
                "started_at": m.started_at,
                "finished_at": m.finished_at,
                "is_active": is_active,
            })
    except Exception:
        pass

    return render(request, "auth/myroom.html", {"room_infos": room_infos})


@api_view(["GET"])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def csrf(request):
    return Response({"csrfToken": get_token(request)})


# =========================
# ✅ 마이페이지 JSON API (수정 완료)
# =========================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def myroom_api(request):
    # [수정] 500 에러의 원인이었던 부분을 now()로 변경
    now = timezone.now()

    participations = (
        Participate.objects
        .filter(user_id=request.user)
        .select_related("meeting", "meeting__room")
        .order_by("meeting__started_at")
    )

    results = []
    seen_meeting_ids = set()

    for p in participations:
        meeting = p.meeting
        room = getattr(meeting, "room", None)
        if not room: continue

        # [수정] DB 시간 데이터와 now를 안전하게 비교
        is_active = False
        if meeting.started_at and meeting.finished_at:
            is_active = meeting.started_at <= now <= meeting.finished_at

        results.append({
            "meeting_id": meeting.id,
            "title": meeting.title,
            "room_name": getattr(room, "name", None),
            "room_slug": getattr(room, "slug", None),
            # 출력 시에만 사용자의 로컬 시간대로 변환
            "started_at": timezone.localtime(meeting.started_at).isoformat() if meeting.started_at else None,
            "finished_at": timezone.localtime(meeting.finished_at).isoformat() if meeting.finished_at else None,
            "is_active": is_active,
        })
        seen_meeting_ids.add(meeting.id)

    # 리더 모임 추가 로직
    try:
        from klub_talk.models import Meeting
        leader_meetings = Meeting.objects.filter(leader_id=request.user).select_related("room").order_by("started_at")
        for m in leader_meetings:
            if m.id in seen_meeting_ids: continue
            room = getattr(m, "room", None)
            if not room: continue

            is_active = (m.started_at <= now <= m.finished_at) if (m.started_at and m.finished_at) else False
            results.append({
                "meeting_id": m.id,
                "title": m.title,
                "room_name": getattr(room, "name", None),
                "room_slug": getattr(room, "slug", None),
                "started_at": timezone.localtime(m.started_at).isoformat() if m.started_at else None,
                "finished_at": timezone.localtime(m.finished_at).isoformat() if m.finished_at else None,
                "is_active": is_active,
            })
    except Exception:
        pass

    results.sort(key=lambda x: x.get("started_at") or "")
    return Response({"results": results}, status=status.HTTP_200_OK)
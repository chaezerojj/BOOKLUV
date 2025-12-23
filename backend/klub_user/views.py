from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone

import requests

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from klub_talk.models import Participate

User = get_user_model()

KAKAO_REST_API_KEY = settings.KAKAO_REST_API_KEY
KAKAO_REDIRECT_URI = settings.KAKAO_REDIRECT_URI
KAKAO_CLIENT_SECRET = settings.KAKAO_CLIENT_SECRET

FRONT_URL = "http://localhost:5173"  # 프론트 주소


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
        # next_url = request.GET.get("state")
        # if next_url:
        #     return redirect(next_url)
        next_url = request.GET.get("state") or f"http://192.168.202.130:8000/api/v1/chat/rooms/"
        return redirect(next_url)

    except Exception as e:
        return JsonResponse({"detail": "callback exception", "error": repr(e)}, status=500)


# =========================
# 프론트용 API (DRF)
# =========================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    """
    프론트에서 세션 로그인 여부 확인용
    GET /api/v1/auth/me/
    """
    user = request.user
    return Response(
        {
            "id": user.id,
            "email": getattr(user, "email", None),
            "kakao_id": getattr(user, "kakao_id", None),
            "username": getattr(user, "username", None),
            "nickname": getattr(user, "nickname", None),
            "is_authenticated": True,
        }
    )


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
    now = timezone.now()

    for p in participations:
        meeting = p.meeting_id
        room = getattr(meeting, "room", None)
        if not room:
            continue

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

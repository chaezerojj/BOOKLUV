import requests
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# 모델 임포트 (프로젝트 구조에 맞게 조정 필요)
from klub_talk.models import Participate, Meeting

User = get_user_model()

# 환경 변수 및 설정값 로드
KAKAO_REST_API_KEY = settings.KAKAO_REST_API_KEY
KAKAO_REDIRECT_URI = settings.KAKAO_REDIRECT_URI
KAKAO_CLIENT_SECRET = settings.KAKAO_CLIENT_SECRET
FRONT_URL = getattr(settings, 'FRONT_URL', 'https://bookluv.netlify.app').rstrip('/')

# =========================
# 1. 카카오 소셜 로그인 (Template & Callback)
# =========================

def auth_login(request):
    """로그인 페이지 렌더링"""
    context = {
        "KAKAO_REST_API_KEY": KAKAO_REST_API_KEY,
        "KAKAO_REDIRECT_URI": KAKAO_REDIRECT_URI,
        "next": request.GET.get("next", ""),
    }
    return render(request, "auth/login.html", context)


def kakao_callback(request):
    """카카오 OAuth 콜백 및 유저 처리"""
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"detail": "missing code"}, status=400)

    try:
        # 1. Access Token 발급
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

        # 2. 사용자 정보 가져오기
        me_res = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=5,
        )

        if me_res.status_code != 200:
            return JsonResponse({"detail": "user info failed", "kakao": me_res.text}, status=400)

        me = me_res.json()
        kakao_id = me.get("id")
        kakao_account = me.get("kakao_account", {})
        email = kakao_account.get("email")

        if not kakao_id:
            return JsonResponse({"detail": "missing kakao id"}, status=400)

        # 3. 유저 생성 또는 조회
        user, _ = User.objects.get_or_create(
            kakao_id=kakao_id,
            defaults={
                "email": email or f"kakao_{kakao_id}@kakao.local",
                "is_active": True,
            },
        )

        # 4. 세션 로그인
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

        # 5. 리다이렉트 (state에 담긴 next_url 혹은 프론트 홈)
        next_url = request.GET.get("state")
        return redirect(next_url if next_url else f"{FRONT_URL}/")

    except Exception as e:
        return JsonResponse({"detail": "callback exception", "error": repr(e)}, status=500)


# =========================
# 2. 사용자 정보 API (DRF)
# =========================

@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user

    if request.method == "GET":
        return Response({
            "id": user.id,
            "email": user.email,
            "nickname": getattr(user, "nickname", ""),
            "is_authenticated": True,
        })

    elif request.method == "PATCH":
        nickname = request.data.get("nickname", "").strip()
        if not nickname:
            return Response({"detail": "nickname is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.nickname = nickname
        user.save(update_fields=["nickname"])
        return Response({"id": user.id, "nickname": user.nickname})


@api_view(["POST"])
def logout_view(request):
    logout(request)
    return Response({"detail": "logged out"})


@api_view(["GET"])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def csrf(request):
    """프론트엔드 CSRF 토큰 발급용"""
    return Response({"csrfToken": get_token(request)})


# =========================
# 3. 마이룸 / 채팅방 목록 API
# =========================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def myroom_api(request):
    """참여 중이거나 방장인 채팅방 목록 JSON 반환"""
    now = timezone.localtime()
    
    # 1. 내가 참여한 모임 조회
    participations = Participate.objects.filter(user_id=request.user).select_related("meeting", "meeting__room")
    
    # 2. 내가 방장인 모임 조회
    leader_meetings = Meeting.objects.filter(leader_id=request.user).select_related("room")

    results = []
    seen_meeting_ids = set()

    def process_meeting(meeting):
        if not meeting or not hasattr(meeting, 'room') or meeting.id in seen_meeting_ids:
            return
        
        room = meeting.room
        started = timezone.localtime(meeting.started_at) if meeting.started_at else None
        finished = timezone.localtime(meeting.finished_at) if meeting.finished_at else None
        
        is_active = False
        if started and finished:
            is_active = started <= now <= finished

        results.append({
            "meeting_id": meeting.id,
            "title": meeting.title,
            "room_name": getattr(room, "name", "알 수 없는 방"),
            "room_slug": getattr(room, "slug", ""),
            "started_at": started.isoformat() if started else None,
            "finished_at": finished.isoformat() if finished else None,
            "is_active": is_active,
        })
        seen_meeting_ids.add(meeting.id)

    # 두 쿼리셋 결과 처리
    for p in participations:
        process_meeting(p.meeting)
    for m in leader_meetings:
        process_meeting(m)

    # 시작 시간 순 정렬
    results.sort(key=lambda x: x.get("started_at") or "")

    return Response({"results": results})
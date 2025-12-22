from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import get_user_model
import requests
from django.contrib.auth import login

User = get_user_model()

KAKAO_REST_API_KEY = settings.KAKAO_REST_API_KEY
KAKAO_REDIRECT_URI = settings.KAKAO_REDIRECT_URI
KAKAO_CLIENT_SECRET = settings.KAKAO_CLIENT_SECRET

def auth_login(request):
    context = {
        "KAKAO_REST_API_KEY": KAKAO_REST_API_KEY,
        "KAKAO_REDIRECT_URI": KAKAO_REDIRECT_URI,
        "next": request.GET.get("next", ""),
    }
    return render(request, 'auth/login.html', context)

FRONT_URL = "http://localhost:5173"  # 프론트 주소

def kakao_callback(request):
    
    code = request.GET.get("code")
    # next_url = request.GET.get("state")
    if not code:
        return JsonResponse({"detail": "missing code", "request": request}, status=400)

    try:
        token_res = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": KAKAO_REST_API_KEY,
                "redirect_uri": KAKAO_REDIRECT_URI,   # http://localhost:8000/api/auth/callback/
                "client_secret": KAKAO_CLIENT_SECRET,
                "code": code,
            },
            timeout=5,
        )
        if token_res.status_code != 200:
            return JsonResponse({"detail": "token exchange failed", "kakao": token_res.text}, status=400)

        access_token = token_res.json().get("access_token")
        if not access_token:
            return JsonResponse({"detail": "no access_token", "kakao": token_res.json()}, status=400)

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
        email = kakao_account.get("email")  # 동의 안 받으면 None

        if not kakao_id:
            return JsonResponse({"detail": "missing kakao id", "me": me}, status=400)

        # 1) 유저 생성/조회 (kakao_id 기준)
        user, created = User.objects.get_or_create(
        kakao_id=kakao_id,
        defaults={
            "email": email or f"kakao_{kakao_id}@kakao.local",
            "is_active": True,
            },
        )
        next_url = request.GET.get("state")
        # 세션 로그인 (핵심)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        if next_url:
            #print(next_url)
            return redirect(next_url)
        return redirect(FRONT_URL + "/")

    except Exception as e:
        return JsonResponse({"detail": "callback exception", "error": repr(e)}, status=500)
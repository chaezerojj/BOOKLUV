import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.conf import settings

KAKAO_REST_API_KEY = settings.KAKAO_REST_API_KEY
KAKAO_REDIRECT_URI = settings.KAKAO_REDIRECT_URI
KAKAO_CLIENT_SECRET = settings.KAKAO_CLIENT_SECRET

@api_view(["GET"])
def login(request):
    context = {
        "KAKAO_REST_API_KEY": KAKAO_REST_API_KEY,
        "KAKAO_REDIRECT_URI": KAKAO_REDIRECT_URI,
    }
    return render(request, 'auth/login.html', context)


# 테스트용 키와 URI 직접 입력

@api_view(["POST"])
def kakao_callback(request):
    code = request.GET.get("code")
    if not code:
        return render(request, "auth/callback.html", {"error": "code 값이 없습니다."})

    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_REST_API_KEY,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code,
        "client_secret": KAKAO_CLIENT_SECRET
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    }

    response = requests.post(url, data=data, headers=headers)

    # 디버그: 응답 출력
    print("status_code:", response.status_code)
    print("response_body:", response.text)

    if response.status_code == 200:
        result = response.json()
        access_token = result.get("access_token")
        refresh_token = result.get("refresh_token")
        context = {"access_token": access_token, "refresh_token": refresh_token}
    else:
        context = {"error": f"토큰 발급 실패: {response.text}"}

    return render(request, "auth/callback.html", context)
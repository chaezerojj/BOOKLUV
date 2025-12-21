import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model, login
from urllib.parse import urlencode

KAKAO_REST_API_KEY = settings.KAKAO_REST_API_KEY
KAKAO_REDIRECT_URI = settings.KAKAO_REDIRECT_URI
KAKAO_CLIENT_SECRET = settings.KAKAO_CLIENT_SECRET

def login(request):
    context = {
        "KAKAO_REST_API_KEY": KAKAO_REST_API_KEY,
        "KAKAO_REDIRECT_URI": KAKAO_REDIRECT_URI,
    }
    return render(request, 'auth/login.html', context)


from django.contrib.auth import get_user_model

User = get_user_model()

def kakao_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "no code"}, status=400)

    # 1️⃣ 토큰 받기
    token_res = requests.post(
        "https://kauth.kakao.com/oauth/token",
        data={
            "grant_type": "authorization_code",
            "client_id": settings.KAKAO_REST_API_KEY,
            "redirect_uri": settings.KAKAO_REDIRECT_URI,
            "code": code,
            "client_secret": settings.KAKAO_CLIENT_SECRET,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    )

    token_res.raise_for_status()
    access_token = token_res.json()["access_token"]

    # 2️⃣ 카카오 유저 정보
    user_res = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    user_res.raise_for_status()
    kakao_user = user_res.json()

    kakao_id = kakao_user["id"]
    kakao_account = kakao_user.get("kakao_account", {})
    email = kakao_account.get("email")  # 없을 수도 있음

    # 3️⃣ 유저 생성 or 조회 (⭐ 핵심 수정)
    user, created = User.objects.get_or_create(
        kakao_id=kakao_id,
        defaults={
            "email": email,
            "is_active": True,
        }
    )

    from rest_framework_simplejwt.tokens import RefreshToken

    refresh = RefreshToken.for_user(user)

     # 5. 프론트로 redirect (토큰 전달)


    # query = urlencode({
    #     "access": str(refresh.access_token),
    #     "refresh": str(refresh),
    # })

    # return redirect(f"http://localhost:8000/auth/callback/?{query}")
    return redirect(f"/auth/callback/?access={refresh.access_token}&refresh={refresh}")

    # return JsonResponse({
    #     "success": True,
    #     "created": created,
    #     "user_id": user.id,
    #     "access": str(refresh.access_token),
    #     "refresh": str(refresh),
    # })





# # 테스트용 키와 URI 직접 입력
# def kakao_callback(request):
#     code = request.GET.get("code")
#     if not code:
#         return JsonResponse({"error": "no code"}, status=400)

#     token_res = requests.post(
#         "https://kauth.kakao.com/oauth/token",
#         data={
#             "grant_type": "authorization_code",
#             "client_id": KAKAO_REST_API_KEY,
#             "redirect_uri": KAKAO_REDIRECT_URI,
#             "client_secret": KAKAO_CLIENT_SECRET,
#             "code": code,
#         },
#         headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
#     )

#     if token_res.status_code != 200:
#         return JsonResponse(token_res.json(), status=400)

#     access_token = token_res.json().get("access_token")

#     user_res = requests.get(
#         "https://kapi.kakao.com/v2/user/me",
#         headers={"Authorization": f"Bearer {access_token}"}
#     )

#     if user_res.status_code != 200:
#         return JsonResponse({"error": "user info failed"}, status=400)

#     kakao_user = user_res.json()
#     kakao_id = kakao_user.get("id")
#     account = kakao_user.get("kakao_account", {})
#     email = account.get("email")
#     #nickname = account.get("profile", {}).get("nickname")

#     User = get_user_model()
#     user, created = User.objects.get_or_create(
#         kakao_id=kakao_id,
#         defaults={
#             #"username": f"kakao_{kakao_id}",
#             "email": email or "",
#             "is_active": True,
#         }
#     )

#     login(request, user)

#     return JsonResponse({
#         "success": True,
#         "created": created,
#         "username": user.username
#     })



    # 여기서 회원가입 / 로그인 처리

    #return JsonResponse({"success": True})



# def kakao_callback(request):
#     code = request.GET.get("code")
#     if not code:
#         return HttpResponseBadRequest("code 없음")
    
#     token_res = requests.post(TOKEN_URL, data=payload)

#     if token_res.status_code != 200:
#         return JsonResponse({
#             "error": "kakao token request failed",
#             "detail": token_res.text
#         }, status=400)

#     token_json = token_res.json()
#     access_token = token_json.get("access_token")


#     # 1. 토큰 요청
#     response = requests.post(...)
#     if response.status_code != 200:
#         return HttpResponse("카카오 토큰 실패", status=400)

#     token = response.json()
#     access_token = token["access_token"]

#     # 2. 사용자 정보 요청
#     profile = requests.get(
#         "https://kapi.kakao.com/v2/user/me",
#         headers={"Authorization": f"Bearer {access_token}"}
#     ).json()

#     # 3. TODO: User 생성 or 로그인 처리

#     # 4. 성공 → 메인 페이지
#     return redirect("/")

'''
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

    # if response.status_code != 200:
    #     return render(
    #         request,
    #         "auth/callback.html",
    #         {"error": f"토큰 발급 실패: {response.text}"}
    #     )

    # result = response.json()
    # access_token = result["access_token"]
    # refresh_token = result.get("refresh_token")


    if response.status_code == 200:
        result = response.json()
        access_token = result.get("access_token")
        refresh_token = result.get("refresh_token")
        context = {"access_token": access_token, "refresh_token": refresh_token}
    else:
        context = {"error": f"토큰 발급 실패: {response.text}"}

    # 추가-사용자 정보 요청
    # user_url = "https://kapi.kakao.com/v2/user/me"
    # user_headers = {
    #     "Authorization": f"Bearer {access_token}",
    #     "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    # }
    # user_response = requests.get(user_url, headers=user_headers)
    # user_info = user_response.json()

    # kakao_id = user_info.get("id")
    # kakao_account = user_info.get("kakao_account", {})
    # email = kakao_account.get("email")
    # profile = kakao_account.get("profile", {})
    # nickname = profile.get("nickname")

    # return render(request, "auth/callback.html", {
    #     "kakao_id": kakao_id,
    #     "email": email,
    #     "nickname": nickname,
    # })

    return render(request, "auth/callback.html", context)


# from allauth.socialaccount.providers.kakao.adapter import KakaoOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView

# from .models import User
# # from .serializers import UserSerializer
# from rest_framework import viewsets, status
# # Create your views here.
# from django.conf import settings
# from allauth.socialaccount.providers.kakao import views as kakao_view
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from rest_framework.decorators import api_view, permission_classes
# from django.http import JsonResponse
# from json.decoder import JSONDecodeError
# from rest_framework.response import Response
# from dj_rest_auth.registration.views import SocialLoginView
# import requests
# from allauth.socialaccount.models import SocialAccount
# from rest_framework.permissions import AllowAny
# from allauth.account.adapter import get_adapter


# class KakaoLogin(SocialLoginView):
#     adapter_class = KakaoOAuth2Adapter
#     callback_url = KAKAO_REDIRECT_URI
#     client_class = OAuth2Client
# class KakaoLoginToDjango(SocialLoginView):
#     adapter_class = KakaoOAuth2Adapter
#     callback_url = KAKAO_REDIRECT_URI
#     client_class = OAuth2Client


# @api_view(['GET'])
# def auth_page(request):
#     return render(request, 'auth.html')     
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny
# from json.decoder import JSONDecodeError
# from rest_framework.response import Response
# import requests
# @api_view(["GET"])
# @permission_classes([AllowAny])
# def kakao_callback(request):
#     rest_api_key = '24dfa2917f81a949062310b5a12ad5ef'  # 카카오 앱키, 추후 시크릿 처리
#     code = request.GET.get("code")
#     print(code)
#     redirect_uri = KAKAO_REDIRECT_URI
#     """
#     Access Token Request
#     """
#     token_req = requests.get(
#         f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}"
#     )
#     token_req_json = token_req.json()
#     error = token_req_json.get("error")
#     if error is not None:
#         raise JSONDecodeError(error)
#     access_token = token_req_json.get("access_token")
#     print(access_token)
#     """
#     Email Request
#     """
#     profile_request = requests.post(
#         "https://kapi.kakao.com/v2/user/me",
#         headers={"Authorization": f"Bearer {access_token}"},
#     )
#     profile_json = profile_request.json()
#     error = profile_json.get("error")
#     if error is not None:
#         raise JSONDecodeError(error)
#     kakao_account = profile_json.get("kakao_account")
#     """
#     kakao_account에서 이메일 외에
#     카카오톡 프로필 이미지, 배경 이미지 url 가져올 수 있음
#     print(kakao_account) 참고
#     """
#     email = kakao_account.get("email")
#     """
#     Signup or Signin Request
#     """


    
#     try:
#         user = User.objects.get(email=email)
#         # 기존에 가입된 유저의 Provider가 kakao가 아니면 에러 발생, 맞으면 로그인
#         # 다른 SNS로 가입된 유저
#         social_user = SocialAccount.objects.get(user=user)
#         if social_user is None:
#             return JsonResponse(
#                 {"err_msg": "email exists but not social user"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         if social_user.provider != "kakao":
#             return JsonResponse(
#                 {"err_msg": "no matching social type"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#         # 기존에 kakao로 가입된 유저
#         data = {"access_token": access_token, "code": code}
#         accept = requests.post(f"{BASE_URL}/accounts/kakao/login/finish/", data=data)
#         # accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
#         accept_status = accept.status_code
#         if accept_status != 200:
#             return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
#         accept_json = accept.json()
#         # refresh_token을 headers 문자열에서 추출함
#         refresh_token = accept.headers['Set-Cookie']
#         refresh_token = refresh_token.replace('=',';').replace(',',';').split(';')
#         token_index = refresh_token.index(' refresh_token')
#         cookie_max_age = 3600 * 24 * 14 # 14 days
#         refresh_token = refresh_token[token_index+1]
#         accept_json.pop("user", None)
#         response_cookie = JsonResponse(accept_json)
#         response_cookie.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
#         return response_cookie
    
#     except User.DoesNotExist:
#         # 기존에 가입된 유저가 없으면 새로 가입
#         data = {"access_token": access_token, "code": code}
#         accept = requests.post(f"{BASE_URL}/accounts/kakao/login/finish/", data=data)
#         # accept = requests.post(f"{BASE_URL}accounts/kakao/login/finish/", data=data)
#         accept_status = accept.status_code
#         if accept_status != 200:
#             return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)
#         # user의 pk, email, first name, last name과 Access Token, Refresh token 가져옴

#         accept_json = accept.json()
#         # refresh_token을 headers 문자열에서 추출함
#         refresh_token = accept.headers['Set-Cookie']
#         refresh_token = refresh_token.replace('=',';').replace(',',';').split(';')
#         token_index = refresh_token.index(' refresh_token')
#         refresh_token = refresh_token[token_index+1]

#         accept_json.pop("user", None)
#         response_cookie = JsonResponse(accept_json)
#         response_cookie.set_cookie('refresh_token', refresh_token, max_age=cookie_max_age, httponly=True, samesite='Lax')
#         return response_cookie
    '''
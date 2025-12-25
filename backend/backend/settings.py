import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# 1. 환경 변수 로드
load_dotenv()

# 2. 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# 3. 보안 설정
SECRET_KEY = os.getenv(
    'SECRET_KEY',
    'django-insecure-v%7qnd++txo72rj^2akf2*)o0(2t7_whrcgcpli6hfp1$g#fvh'
)

# 운영 환경에서는 반드시 False가 되도록 설정 (환경 변수 DEBUG=True 가 아니면 False)
DEBUG = os.getenv('DEBUG', 'False').lower() in ('1', 'true', 'yes')

# 4. 호스트 및 도메인 설정
# 환경 변수에 ALLOWED_HOSTS가 없으면 기본 도메인들을 사용
DEFAULT_HOSTS = 'bookluv.railway.app,localhost,127.0.0.1'
ALLOWED_HOSTS = [
    'bookluv.com',
    '.railway.app',  # Railway에서 제공하는 모든 서브도메인 허용
    'localhost',
    '127.0.0.1',
]
# 서비스 메인 도메인 설정 (리다이렉트 시 활용)
BASE_URL = os.getenv('DOMAIN_URL', 'https://bookluv-production.up.railway.app/').rstrip('/')

# 5. 애플리케이션 정의
INSTALLED_APPS = [
    'daphne',          # ASGI 처리를 위해 반드시 최상단에 위치
    'drf_yasg',
    'django_extensions',
    'corsheaders',
    'channels',        # 웹소켓용
    'klub_board',
    'klub_chat',
    'klub_talk',
    'klub_user',
    'klub_recommend',
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

# 6. 미들웨어 설정 (순서가 매우 중요함)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',    # 1순위
    'corsheaders.middleware.CorsMiddleware',            # CORS
    'whitenoise.middleware.WhiteNoiseMiddleware',       # 정적 파일 서빙
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 7. 서버 실행 방식 (WSGI & ASGI)
WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION = "backend.asgi.application"

# 8. 데이터베이스 설정 (Railway DATABASE_URL 우선 사용)
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# 9. Redis 및 채널 레이어 설정 (웹소켓용)
REDIS_URL = os.getenv('REDIS_URL', 'redis://default:bGBSgqYKpfUrphgGUScwxHlFkdvRIKYh@redis.railway.internal:6379')
#-------------------------------------------
if REDIS_URL:
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [REDIS_URL]},
        }
    }
else:
    # Redis 없으면 개발용으로라도 서버가 죽지 않게
    CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
#-------------------------------------------
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [REDIS_URL], # 여기서 비밀번호가 포함된 URL이 들어가야 합니다.
#         },
#     },
# }

# Celery 설정
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', CELERY_BROKER_URL)

# 10. 정적 및 미디어 파일 설정
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# WhiteNoise가 정적 파일을 압축 및 캐싱하도록 설정
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 11. 인증 및 소셜 로그인 설정
AUTH_USER_MODEL = 'klub_user.User'
SITE_ID = int(os.getenv('SITE_ID', '1'))

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# 로그인 관련 URL (IP 주소 대신 BASE_URL 사용)
LOGIN_URL = f"{BASE_URL}/api/v1/auth/"
LOGIN_REDIRECT_URL = f"{BASE_URL}/api/v1/chat/rooms/"

# 프론트 주소 (OAuth 콜백 후 리다이렉트용)
FRONT_URL = os.getenv('FRONT_URL', 'https://bookluv.netlify.app').rstrip('/')

# 카카오 로그인 설정
KAKAO_REST_API_KEY = os.getenv('KAKAO_REST_API_KEY', '4bf9c626d2f496b06164d72b26db4b81')
KAKAO_CLIENT_SECRET = os.getenv('KAKAO_CLIENT_SECRET', 'Py28EL9FRcSyE0PYtkz0TpKTCAjmdUwZ')
KAKAO_REDIRECT_URI = os.getenv('KAKAO_REDIRECT_URI', f"{BASE_URL}/api/v1/auth/callback/")

# 콜백 URI에 'callback'이 포함되어 있지 않으면 자동으로 추가
if 'callback' not in KAKAO_REDIRECT_URI:
    if KAKAO_REDIRECT_URI.endswith('/'):
        KAKAO_REDIRECT_URI = KAKAO_REDIRECT_URI + 'callback/'
    else:
        KAKAO_REDIRECT_URI = KAKAO_REDIRECT_URI + '/callback/'


# 12. CORS 및 CSRF 신뢰 도메인
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    "https://*.railway.app",
    "https://bookluv.netlify.app", 
]
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://bookluv.netlify.app",
    "https://*.railway.app",
    "https://*.netlify.app",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https:\/\/.*\.railway\.app$",
    r"^https:\/\/.*\.netlify\.app$",
]

# 13. 국제화 설정
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 14. 실서비스 보안 설정 (HTTPS 전용)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True

    # cross-site cookie 허용 (세션/CSRF)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SAMESITE = "None"
else:
    # 로컬(http) 개발 편하게
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"

# GMS API 등 외부 서비스 설정
GMS_API_KEY = os.getenv("GMS_KEY")
GMS_OPENAI_URL = os.getenv("GMS_OPENAI_URL", "https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions")

# (선택) 프론트 JS가 csrf 쿠키 읽게 하려면 (기본 False라 대개 OK)
CSRF_COOKIE_HTTPONLY = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
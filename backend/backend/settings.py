import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# 1. 환경 변수 로드
load_dotenv()

# 2. 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent

# 3. 보안 설정
SECRET_KEY = os.getenv('SECRET_KEY')

# 운영 환경에서는 반드시 False가 되도록 설정
DEBUG = os.getenv('DEBUG', 'False').lower() in ('1', 'true', 'yes')

# 4. 호스트 및 도메인 설정
# 환경 변수에서 쉼표로 구분된 문자열을 받아 리스트로 변환
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# 서비스 메인 도메인 설정 (리다이렉트 시 활용)
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000').rstrip('/')

# 5. 애플리케이션 정의
INSTALLED_APPS = [
    'daphne',
    'drf_yasg',
    'django_extensions',
    'corsheaders',
    'channels',
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

# 6. 미들웨어 설정
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION = "backend.asgi.application"

# 8. 데이터베이스 설정 (Railway 등 환경변수 우선)
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

# 9. Redis 및 채널 레이어 설정
REDIS_URL = os.getenv('REDIS_URL')
if REDIS_URL:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [REDIS_URL]},
        }
    }
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
else:
    CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# 10. 정적 및 미디어 파일
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 11. 인증 및 소셜 로그인
AUTH_USER_MODEL = 'klub_user.User'
SITE_ID = int(os.getenv('SITE_ID', '1'))

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_URL = f"{BASE_URL}/api/v1/auth/"
LOGIN_REDIRECT_URL = f"{BASE_URL}/api/v1/chat/rooms/"
FRONT_URL = os.getenv('FRONT_URL', 'https://bookluv.netlify.app').rstrip('/')

# 카카오 로그인 (모두 환경변수 처리)
KAKAO_REST_API_KEY = os.getenv('KAKAO_REST_API_KEY')
KAKAO_CLIENT_SECRET = os.getenv('KAKAO_CLIENT_SECRET')
KAKAO_REDIRECT_URI = os.getenv('KAKAO_REDIRECT_URI', f"{BASE_URL}/api/v1/auth/callback/")

# 12. CORS 및 CSRF 설정 (환경변수에서 리스트로 가져오기)
def get_env_list(var_name, default=""):
    val = os.getenv(var_name, default)
    return [i.strip() for i in val.split(",") if i.strip()]

CORS_ALLOWED_ORIGINS = get_env_list('CORS_ALLOWED_ORIGINS')
CSRF_TRUSTED_ORIGINS = get_env_list('CSRF_TRUSTED_ORIGINS')

CORS_ALLOW_CREDENTIALS = True
WHITENOISE_MANIFEST_STRICT = False

# 13. 국제화
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 14. 보안 및 HTTPS
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = "None"
    CSRF_COOKIE_SAMESITE = "None"
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SAMESITE = "Lax"

# 외부 서비스
GMS_API_KEY = os.getenv("GMS_KEY")
GMS_OPENAI_URL = os.getenv("GMS_OPENAI_URL")

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_PARSER_CLASSES': ('rest_framework.parsers.JSONParser',),
}
import os
from pathlib import Path
from dotenv import load_dotenv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v%7qnd++txo72rj^2akf2*)o0(2t7_whrcgcpli6hfp1$g#fvh'

CELERY_BROKER_URL = 'redis://redis:6379/0'  # 'localhost'를 'redis'로 변경
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'  # 'localhost'를 'redis'로 변경

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# 로그인 페이지 URL
LOGIN_URL = 'http://192.168.202.130:8000/api/v1/auth/'

# 로그인 성공 후 기본 리다이렉트
LOGIN_REDIRECT_URL = 'http://192.168.202.130:8000/api/v1/chat/rooms/'

load_dotenv()

# Application definition

GMS_API_KEY = os.getenv("GMS_KEY")
GMS_OPENAI_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions"

INSTALLED_APPS = [
    'drf_yasg',
    "django_extensions",
    'corsheaders',
    'channels',
    'daphne',
    'klub_board',
    'klub_chat',
    'klub_talk',
    'klub_user',
    "klub_recommend",
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites', # 필수
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]

ASGI_APPLICATION = "backend.asgi.application"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],  # 로컬 환경에서는 이렇게 설정해야 합니다.
        },
    },
}


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
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


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # 개발 중인 프론트엔드 서버
    'https://your-frontend-domain.com',  # 배포된 프론트엔드 서버
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://glycogenetic-stilted-sunshine.ngrok-free.dev",  # ngrok 도메인 추가
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://glycogenetic-stilted-sunshine.ngrok-free.dev",  # ngrok 도메인 추가
]


# settings.py

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#     'file': {
#         'level': 'DEBUG',
#         'class': 'logging.handlers.RotatingFileHandler',
#         'filename': 'chat_log.txt',
#         'maxBytes': 10485760,  # 파일 최대 크기 10MB
#         'backupCount': 5,  # 최대 5개의 백업 파일 유지
#         },
#     },

#     'loggers': {
#         'django': {
#             'handlers': ['file'],  # 콘솔과 파일 두 곳에 로그 기록
#             'level': 'DEBUG',  # DEBUG 레벨로 모든 로그 기록
#             'propagate': True,
#         },
#         'channels': {
#             'handlers': ['file'],  # channels 로그도 콘솔과 파일에 기록
#             'level': 'DEBUG',  # DEBUG 레벨로 기록
#             'propagate': True,
#         },
#     },
# }

KAKAO_REST_API_KEY = '4bf9c626d2f496b06164d72b26db4b81'
KAKAO_REDIRECT_URI = 'https://dayle-preadherent-longly.ngrok-free.dev/api/v1/auth/callback/'
KAKAO_CLIENT_SECRET = 'Py28EL9FRcSyE0PYtkz0TpKTCAjmdUwZ'


SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
AUTH_USER_MODEL = 'klub_user.User'

CORS_ALLOW_CREDENTIALS = True

# 개발환경(HTTP)에서 프론트<->백엔드 다른 포트면 SameSite 이슈 있어서 설정
# 세션 쿠키를 프론트에서도 쓰게 할 때 (필요하다면..)

LOGIN_URL = "https://dayle-preadherent-longly.ngrok-free.dev/api/v1/auth/"

ALLOWED_HOSTS = ['*']
DOMAIN_URL = "https://dayle-preadherent-longly.ngrok-free.dev/"

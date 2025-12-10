from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('klub_chat.urls')),  # 여기선 include만 해도 app_name이 있으면 namespace 사용 가능
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/talk/', include('klub_talk.urls')),
    path('api/chat/', include('klub_chat.urls')),
]

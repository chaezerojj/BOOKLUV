from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin', admin.site.urls),
    path('api/v1', include('klub_talk.urls')), 
    path('api/chat', include('klub_chat.urls')), 
    path("api/recommend/", include("klub_recommend.urls")),
]

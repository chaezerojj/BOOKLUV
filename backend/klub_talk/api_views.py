from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer  # 네 프로젝트에 맞는 serializer 사용

# 모임 모델 위치에 맞게 import 수정
from klub_talk.models import Meeting  # <- 실제 위치가 다르면 수정!

@api_view(["GET"])
def book_search_api(request):
    q = (request.GET.get("q") or "").strip()
    qs = Book.objects.all()

    if q:
        qs = qs.filter(title__icontains=q)

    return Response(BookSerializer(qs, many=True).data)

@api_view(["GET"])
def book_detail_api(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    # ✅ Meeting FK 이름에 맞게 수정 (예: book_id / book)
    meetings_qs = Meeting.objects.filter(book_id=book_id).order_by("-id")

    meetings = [
        {
            "id": m.id,
            "title": m.title,
            "members": getattr(m, "members", 0),
            "views": getattr(m, "views", 0),
            "description": getattr(m, "description", ""),
        }
        for m in meetings_qs
    ]

    return Response({
        "book": BookSerializer(book).data,
        "meetings": meetings,
    })

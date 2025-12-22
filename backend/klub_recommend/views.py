import json
import traceback
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from klub_talk.models import Book, Category
from .models import ReadingPreference, RecommendationResult
from .services.openai_client import get_ai_recommendation

GENRE_MAP = {
    "A": "소설/시/희곡",
    "B": "자기계발",
    "C": "인문학",
    "D": "SF/판타지/추리",
}

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def result_api_view(request):
    print("==================================================")
    print("AUTH:", request.user, request.user.is_authenticated)
    print("DATA:", request.data)
    print("==================================================")

    data = request.data

    q4 = data.get("q4")
    category_name = GENRE_MAP.get(q4)
    if not category_name:
        return Response(
            {"detail": "선호 장르(q4)가 올바르지 않습니다."},
            status=status.HTTP_400_BAD_REQUEST
        )

    quiz_answers = {
        "목적": data.get("q1"),
        "신간_고전": data.get("q2"),
        "선호_장르": q4,
        "분량": data.get("q7"),
        "독서스타일": data.get("q8"),
        "필요한책": data.get("q10"),
        "선호_장르_이름": category_name,
    }

    categories = Category.objects.filter(name=category_name)
    all_candidate_books = Book.objects.filter(category_id__in=categories).select_related("author_id", "category_id")

    if not all_candidate_books.exists():
        return Response({"ai_reason": "현재 추천 가능한 도서가 없습니다.", "books": []}, status=200)

    books_for_ai = all_candidate_books[:20]

    # ✅ OpenAI 호출 자체도 예외 처리 (여기가 500 제일 흔함)
    try:
        ai_response = get_ai_recommendation(quiz_answers, books_for_ai)
    except Exception as e:
        print("❌ get_ai_recommendation ERROR:", repr(e))
        traceback.print_exc()
        ai_response = "{}"

    try:
        parsed = json.loads(ai_response) if ai_response else {}
    except json.JSONDecodeError:
        parsed = {}

    ai_reason = parsed.get("ai_reason", "사용자님의 성향을 분석한 결과입니다.")
    reco_data = parsed.get("recommendations", [])

    suggested_id = reco_data[0].get("book_id") if reco_data else None
    recommended_book_qs = all_candidate_books.filter(id=suggested_id)

    if recommended_book_qs.exists():
        final_book = recommended_book_qs[0]
        temp_reason = reco_data[0].get("reason")
    else:
        final_book = all_candidate_books.first()
        temp_reason = (
            f"사용자님이 선호하시는 장르는 {category_name}입니다. "
            f"오늘 '{final_book.title}'은 어떠실까요?"
        )

    # ✅ author/category NULL-safe
    author_name = final_book.author_id.name if final_book.author_id else None
    category_name_safe = final_book.category_id.name if final_book.category_id else None

    user = request.user

    # ✅ 혹시 None 들어가면 DB에서 500 날 수 있으니 기본값도 방어
    pref = ReadingPreference.objects.create(
        user=user,
        purpose=data.get("q1") or "",
        new_vs_classic=data.get("q2") or "",
        category=data.get("q4") or "",
        mood=data.get("q5") or "",
        reading_style=data.get("q8") or "",
        length_pref=data.get("q7") or "",
        difficulty_pref=data.get("q6") or "",
    )

    result_obj = RecommendationResult.objects.create(
        user=user,
        preference=pref,
        ai_reason=ai_reason
    )
    result_obj.books.set([final_book])

    return Response({
        "ai_reason": ai_reason,
        "books": [{
            "id": final_book.id,
            "title": final_book.title,
            "cover_url": final_book.cover_url,
            "publisher": final_book.publisher,
            "author_name": author_name,
            "category_name": category_name_safe,
            "reason": temp_reason,
        }]
    }, status=200)

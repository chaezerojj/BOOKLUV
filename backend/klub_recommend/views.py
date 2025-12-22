import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from klub_talk.models import Book, Category
from klub_user.models import User
from .models import ReadingPreference, RecommendationResult
from .services.openai_client import get_ai_recommendation

GENRE_MAP = {
    "A": "소설/시/희곡",
    "B": "자기계발",
    "C": "인문학",
    "D": "SF/판타지/추리",
}

@api_view(["POST"])
@permission_classes([AllowAny])  # 로그인 필수로 할 거면 AllowAny 대신 IsAuthenticated로 바꿔
def result_api_view(request):
    data = request.data  # ✅ Vue(JSON)도 여기로 들어옴

    # 1) 퀴즈 응답 수집 (기존 코드와 동일한 키 구조)
    quiz_answers = {
        "목적": data.get("q1"),
        "신간_고전": data.get("q2"),
        "선호_장르": data.get("q4"),
        "분량": data.get("q7"),
        "독서스타일": data.get("q8"),
        "필요한책": data.get("q10"),
    }

    # 2) 카테고리 필터링 및 후보군 추출
    category_name = GENRE_MAP.get(data.get("q4"))
    quiz_answers["선호_장르_이름"] = category_name

    categories = Category.objects.filter(name=category_name)
    all_candidate_books = Book.objects.filter(category_id__in=categories)

    if not all_candidate_books.exists():
        return Response({
            "ai_reason": "현재 추천 가능한 도서가 없습니다.",
            "books": []
        }, status=200)

    books_for_ai = all_candidate_books[:20]

    # 3) GPT 추천 요청
    ai_response = get_ai_recommendation(quiz_answers, books_for_ai)

    try:
        parsed = json.loads(ai_response)
    except json.JSONDecodeError:
        # GPT가 JSON 깨서 보내는 경우 방어
        parsed = {}

    ai_reason = parsed.get("ai_reason", "사용자님의 성향을 분석한 결과입니다.")
    reco_data = parsed.get("recommendations", [])

    # 4) 추천 book_id 검증
    suggested_id = reco_data[0].get("book_id") if reco_data else None
    recommended_book_qs = all_candidate_books.filter(id=suggested_id).select_related("author_id", "category_id")

    if recommended_book_qs.exists():
        final_book = recommended_book_qs[0]
        temp_reason = reco_data[0].get("reason")
    else:
        final_book = list(all_candidate_books[:1])[0]
        temp_reason = (
            f"사용자님이 선호하시는 장르는 {category_name}입니다. "
            f"이 책은 사용자의 취향을 반영한 깊이 있는 이야기를 담고 있습니다. "
            f"새로운 영감이 필요하다면 오늘 '{final_book.title}'은 어떠실까요?"
        )

    # 5) DB 저장 로직 (기존과 동일)
    user = request.user if request.user.is_authenticated else User.objects.first()

    pref = ReadingPreference.objects.create(
        user=user,
        purpose=quiz_answers["목적"],
        new_vs_classic=quiz_answers["신간_고전"],
        category=quiz_answers["선호_장르"],
        mood=data.get("q5"),
        reading_style=quiz_answers["독서스타일"],
        length_pref=quiz_answers["분량"],
        difficulty_pref=data.get("q6"),
    )

    result_obj = RecommendationResult.objects.create(
        user=user, preference=pref, ai_reason=ai_reason
    )
    result_obj.books.set([final_book])

    # 6) JSON으로 반환
    return Response({
        "ai_reason": ai_reason,
        "books": [{
            "id": final_book.id,
            "title": final_book.title,
            "cover_url": final_book.cover_url,
            "publisher": final_book.publisher,
            "author_name": final_book.author_id.name,
            "category_name": final_book.category_id.name,
            "reason": temp_reason,
        }]
    }, status=200)

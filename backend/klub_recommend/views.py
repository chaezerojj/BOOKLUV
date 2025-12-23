import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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

@api_view(["GET"])
def quiz_view(request):
    return render(request, "recommend/quiz.html")

@api_view(["GET", "POST"])
def result_view(request):
    # ✅ GET: 기존처럼 HTML 화면 유지(원하면 삭제 가능)
    if request.method == "GET":
        return render(request, "recommend/quiz.html")

    # ✅ POST: Vue에서 보내는 JSON은 request.data로 받기
    payload = request.data or {}

    # 1) 퀴즈 응답 수집 (request.POST -> payload)
    quiz_answers = {
        "목적": payload.get("q1"),
        "신간_고전": payload.get("q2"),
        "선호_장르": payload.get("q4"),
        "분량": payload.get("q7"),
        "독서스타일": payload.get("q8"),
        "필요한책": payload.get("q10"),
    }

    category_name = GENRE_MAP.get(payload.get("q4"))
    quiz_answers["선호_장르_이름"] = category_name

    if not category_name:
        return Response(
            {"ai_reason": "선호 장르가 선택되지 않았습니다.", "books": []},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 2) 후보군 추출
    categories = Category.objects.filter(name=category_name)
    all_candidate_books = Book.objects.filter(category_id__in=categories)

    if not all_candidate_books.exists():
        # ✅ JSON으로 반환
        return Response(
            {"ai_reason": "현재 추천 가능한 도서가 없습니다.", "books": []},
            status=status.HTTP_200_OK,
        )

    books_for_ai = all_candidate_books[:20]

    # 3) GPT 추천 요청
    ai_response = get_ai_recommendation(quiz_answers, books_for_ai)

    try:
        parsed = json.loads(ai_response)
    except json.JSONDecodeError:
        # AI 응답이 깨졌을 때 fallback
        final_book = all_candidate_books.first()
        return Response(
            {
                "ai_reason": "추천 생성 중 문제가 발생해 기본 추천을 제공해요.",
                "books": [{
                    "id": final_book.id,
                    "title": final_book.title,
                    "cover_url": getattr(final_book, "cover_url", None),
                    "author_name": getattr(getattr(final_book, "author_id", None), "name", None),
                    "publisher": getattr(final_book, "publisher", None),
                    "category_name": category_name,
                    "reason": f"사용자님이 선호하시는 장르는 {category_name}입니다.",
                }],
            },
            status=status.HTTP_200_OK,
        )

    ai_reason = parsed.get("ai_reason", "사용자님의 성향을 분석한 결과입니다.")
    reco_data = parsed.get("recommendations", [])

    suggested_id = reco_data[0].get("book_id") if reco_data else None
    recommended_book_qs = all_candidate_books.filter(id=suggested_id).select_related('author_id', 'category_id')

    if recommended_book_qs.exists():
        final_book = recommended_book_qs[0]
        reason = reco_data[0].get("reason")
    else:
        final_book = all_candidate_books.first()
        reason = (
            f"사용자님이 선호하시는 장르는 {category_name}입니다. "
            f"오늘 '{final_book.title}'은 어떠실까요?"
        )

    # 4) DB 저장 로직 (payload.get 사용)
    user = request.user if request.user.is_authenticated else User.objects.first()

    pref = ReadingPreference.objects.create(
        user=user,
        purpose=quiz_answers["목적"],
        new_vs_classic=quiz_answers["신간_고전"],
        category=quiz_answers["선호_장르"],
        mood=payload.get("q5"),
        reading_style=quiz_answers["독서스타일"],
        length_pref=quiz_answers["분량"],
        difficulty_pref=payload.get("q6"),
    )

    result_obj = RecommendationResult.objects.create(
        user=user, preference=pref, ai_reason=ai_reason
    )
    result_obj.books.set([final_book])

    # ✅ 5) Vue가 바로 쓸 JSON 응답 형태로 반환
    return Response(
        {
            "ai_reason": ai_reason,
            "books": [
                {
                    "id": final_book.id,
                    "title": final_book.title,
                    "cover_url": getattr(final_book, "cover_url", None),
                    "author_name": getattr(getattr(final_book, "author_id", None), "name", None),
                    "publisher": getattr(final_book, "publisher", None),
                    "category_name": category_name,
                    "reason": reason,
                }
            ],
        },
        status=status.HTTP_200_OK,
    )

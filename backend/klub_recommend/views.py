import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from klub_talk.models import Book, Category
from rest_framework.decorators import api_view, renderer_classes  # renderer_classes 추가
from rest_framework.renderers import JSONRenderer              # JSONRenderer 추가
from .models import ReadingPreference, RecommendationResult
from .services.openai_client import get_ai_recommendation
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

GENRE_MAP = {
    "novel": "소설",
    "essay": "에세이",
    "self_help": "자기계발",
    "humanities": "인문학",
    "art": "예술",
}

@api_view(["GET"])
def quiz_view(request):
    return render(request, "recommend/quiz.html")

# 수정된 GENRE_MAP (DB의 Category 테이블 name 컬럼과 정확히 일치해야 함)
GENRE_MAP = {
    "novel": "소설",
    "essay": "에세이",
    "self_help": "자기계발",
    "humanities": "인문/사회", # 예시: DB에 '인문/사회'로 저장된 경우
    "science": "과학",
    "art": "예술",
    "economy": "경제경영"
}

@api_view(["GET", "POST"])
@renderer_classes([JSONRenderer])
def result_view(request):
    if request.method == "GET":
        return render(request, "recommend/quiz.html")

    data = request.data or request.POST
    
    # 4번 문항 선택값 가져오기
    selected_genre_key = data.get("q4") 
    category_name = GENRE_MAP.get(selected_genre_key)

    # 1. 카테고리 유효성 검사
    if not category_name:
        return Response({
            "ai_reason": "장르 선택값이 올바르지 않습니다.",
            "books": []
        }, status=400)

    # 2. DB 조회 (PostgreSQL의 klub_talk_category 참조)
    categories = Category.objects.filter(name=category_name)
    print(f"DEBUG: Selected Category Name -> {category_name}")
    print(f"DEBUG: Found Categories -> {categories}")

    all_candidate_books = Book.objects.filter(category_id__in=categories)

    # 3. 도서 존재 여부 체크
    if not all_candidate_books.exists():
        return Response({
            "ai_reason": f"죄송합니다. '{category_name}' 장르에 해당하는 도서 데이터가 없습니다.",
            "books": []
        }, status=200)

    # ✅ 기본 fallback
    final_book = all_candidate_books.first()
    ai_reason = "사용자님의 성향을 분석한 결과입니다."
    reco_data = []
    
    print(final_book)

    # ✅ AI 실패해도 500 안나게
    try:
        ai_response = get_ai_recommendation(quiz_answers, all_candidate_books[:20])
        parsed = json.loads(ai_response)
        ai_reason = parsed.get("ai_reason", ai_reason)
        reco_data = parsed.get("recommendations", []) or []

        suggested_id = reco_data[0].get("book_id") if reco_data else None
        if suggested_id:
            pick = all_candidate_books.filter(id=suggested_id).first()
            if pick:
                final_book = pick
    except Exception as e:
        ai_reason = f"AI 추천에 실패하여 기본 추천을 보여드립니다. ({type(e).__name__})"

    # 템플릿용 추천 이유
    if reco_data and final_book and final_book.id == reco_data[0].get("book_id"):
        final_book.temp_reason = reco_data[0].get("reason")
    else:
        final_book.temp_reason = (
            f"선호 장르({category_name}) 기반 기본 추천입니다."
        )

    # ✅ DB 저장은 로그인일 때만(또는 게스트 유저를 확실히 보장)
    if request.user.is_authenticated:
        try:
            pref = ReadingPreference.objects.create(
                user=request.user,
                purpose=quiz_answers["목적"],
                new_vs_classic=quiz_answers["신간_고전"],
                category=quiz_answers["선호_장르"],
                mood=data.get("q5"),
                reading_style=quiz_answers["독서스타일"],
                length_pref=quiz_answers["분량"],
                difficulty_pref=data.get("q6"),
            )
            result_obj = RecommendationResult.objects.create(
                user=request.user, preference=pref, ai_reason=ai_reason
            )
            result_obj.books.set([final_book])
        except Exception:
            pass

    payload = {
        "ai_reason": ai_reason,
        "books": [
            {
                "id": final_book.id,
                "title": final_book.title,
                "publisher": final_book.publisher,
                "cover_url": final_book.cover_url,
                "author_name": getattr(final_book.author_id, "name", None),
                "category_name": getattr(final_book.category_id, "name", None),
                "reason": getattr(final_book, "temp_reason", None),
            }
        ],
    }
    
    return Response(payload)
    # return Response(payload, status=status.HTTP_200_OK)
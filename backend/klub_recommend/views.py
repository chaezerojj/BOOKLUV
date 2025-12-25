import json
from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from klub_talk.models import Book, Category
from .models import ReadingPreference, RecommendationResult
from .services.openai_client import get_ai_recommendation

# 1. 페이지 접속용 (기존 유지)
def quiz_view(request):
    return render(request, "recommend/quiz.html")

# 2. 결과 API (완전한 API 형태로 수정)
@api_view(["POST"]) # GET 요청을 아예 받지 않도록 제한
@renderer_classes([JSONRenderer])
def result_view(request):
    # DRF에서는 request.data를 사용합니다.
    data = request.data
    
    GENRE_MAP = {
        "novel": ["소설/시/희곡"],
        "essay": ["에세이"],
        "self_help": ["자기계발"],
        "humanities": ["인문학", "사회과학"],
        "science": ["과학"],
        "art": ["예술/대중문화"],
        "economy": ["경제경영"],
        "life": ["요리/살림"],
    }
    
    selected_genre_key = data.get("q4")
    category_list = GENRE_MAP.get(selected_genre_key, [])

    if not category_list:
        return Response({"ai_reason": "장르 정보가 누락되었습니다.", "books": []}, status=400)

    # DB 조회
    categories = Category.objects.filter(name__in=category_list)
    all_candidate_books = Book.objects.filter(category_id__in=categories)

    if not all_candidate_books.exists():
        return Response({
            "ai_reason": f"'{'/'.join(category_list)}' 장르의 도서 데이터가 없습니다.",
            "books": []
        }, status=200)

    # 기본값 설정
    final_book = all_candidate_books.first()
    ai_reason = "사용자 성향 분석 결과입니다."
    temp_reason = "추천 도서입니다."

    # AI 로직 (예외 처리 강화)
    try:
        quiz_answers = {
            "목적": data.get("q1"),
            "선호_장르": "/".join(category_list),
            "분위기": data.get("q5"),
        }
        ai_response = get_ai_recommendation(quiz_answers, all_candidate_books[:20])
        parsed = json.loads(ai_response)
        ai_reason = parsed.get("ai_reason", ai_reason)
        reco_data = parsed.get("recommendations", [])

        if reco_data:
            suggested_id = reco_data[0].get("book_id")
            pick = all_candidate_books.filter(id=suggested_id).first()
            if pick:
                final_book = pick
                temp_reason = reco_data[0].get("reason", temp_reason)
    except Exception as e:
        print(f"AI Error: {e}")

    # 데이터 구성 (안전하게 getattr 사용)
    payload = {
        "ai_reason": ai_reason,
        "books": [{
            "id": final_book.id,
            "title": final_book.title,
            "publisher": final_book.publisher,
            "cover_url": final_book.cover_url,
            "author_name": getattr(final_book.author_id, "name", "저자 미상"),
            "category_name": getattr(final_book.category_id, "name", "장르 미상"),
            "reason": temp_reason,
        }],
    }

    return Response(payload, status=200)
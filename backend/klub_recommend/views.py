import json
from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from klub_talk.models import Book, Category
from .services.openai_client import get_ai_recommendation

# 1. 페이지 접속용 (기존 유지)
def quiz_view(request):
    return render(request, "recommend/quiz.html")


@api_view(["POST"])
@renderer_classes([JSONRenderer])
def result_view(request):
    # 1. 안전하게 데이터 가져오기
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

    # 2. 결과가 없을 경우 대비
    categories = Category.objects.filter(name__in=category_list)
    all_candidate_books = Book.objects.filter(category_id__in=categories)

    if not all_candidate_books.exists():
        return Response({
            "ai_reason": "선택하신 장르의 도서를 준비 중입니다.",
            "books": []
        }, status=200)

    # 3. 기본값 설정
    final_book = all_candidate_books.first()
    ai_reason = "사용자님의 성향을 분석한 결과입니다."
    temp_reason = "추천드리는 도서입니다."

    # 4. AI 로직 (예외 발생 시 서버가 죽지 않도록 try-except)
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
        print(f"AI 분석 실패: {e}") # Railway 로그에 찍힘

    # 5. 응답 생성 (getattr로 데이터 누락 방어)
    payload = {
        "ai_reason": ai_reason,
        "books": [
            {
                "id": final_book.id,
                "title": final_book.title,
                "publisher": final_book.publisher,
                "cover_url": final_book.cover_url,
                "author_name": getattr(final_book.author_id, "name", "저자 미상"),
                "category_name": getattr(final_book.category_id, "name", "장르 미상"),
                "reason": temp_reason, 
            }
        ],
    }

    return Response(payload, status=200)
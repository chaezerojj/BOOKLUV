import json
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
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
def result_view(request):
    """
    사용자의 퀴즈 답변을 받아 AI 추천 결과를 JSON으로 반환합니다.
    """
    data = request.data  # Pinia에서 보낸 JSON 데이터
    
    # 1. 장르 매핑 및 유효성 검사
    genre_code = data.get("q4")
    category_name = GENRE_MAP.get(genre_code)
    
    if not category_name:
        return Response({
            "error": "Invalid Genre",
            "ai_reason": "장르 선택값이 올바르지 않습니다.",
            "books": []
        }, status=status.HTTP_400_BAD_REQUEST)

    # 2. 추천 후보 도서 추출 (해당 카테고리의 책들)
    categories = Category.objects.filter(name=category_name)
    all_candidate_books = Book.objects.filter(category_id__in=categories)

    if not all_candidate_books.exists():
        return Response({
            "ai_reason": "현재 해당 장르에 추천 가능한 도서가 없습니다.",
            "books": []
        }, status=status.HTTP_200_OK)

    # 3. 기본값 설정 (AI 실패 대비)
    final_book = all_candidate_books.first()
    ai_reason = "사용자님의 성향을 분석한 결과입니다."
    temp_reason = f"선호 장르({category_name}) 기반 기본 추천입니다."

    # 4. AI 추천 로직 실행
    quiz_answers = {
        "선호_장르_이름": category_name,
        "목적": data.get("q1"),
        "신간_고전": data.get("q2"),
        "선호_장르": genre_code,
        "mood": data.get("q5"),
        "분량": data.get("q7"),
        "독서스타일": data.get("q8"),
        "필요한책": data.get("q10"),
    }

    try:
        # 최대 20권의 후보를 AI에게 전달
        ai_response = get_ai_recommendation(quiz_answers, all_candidate_books[:20])
        parsed = json.loads(ai_response)
        
        ai_reason = parsed.get("ai_reason", ai_reason)
        reco_list = parsed.get("recommendations", [])

        if reco_list:
            suggested_id = reco_list[0].get("book_id")
            # AI가 추천한 ID가 실제 후보군에 있는지 확인
            pick = all_candidate_books.filter(id=suggested_id).first()
            if pick:
                final_book = pick
                temp_reason = reco_list[0].get("reason", temp_reason)
                
    except Exception as e:
        # AI 오류 시 로그를 남기고 기본값 유지
        print(f"AI Recommendation Error: {e}")
        ai_reason = f"AI 추천 서비스가 잠시 지연되어 기본 추천을 제공합니다."

    # 5. DB 저장 (로그인 사용자일 경우에만)
    if request.user.is_authenticated:
        try:
            pref = ReadingPreference.objects.create(
                user=request.user,
                purpose=quiz_answers["목적"],
                new_vs_classic=quiz_answers["신간_고전"],
                category=quiz_answers["선호_장르"],
                mood=quiz_answers["mood"],
                reading_style=quiz_answers["독서스타일"],
                length_pref=quiz_answers["분량"],
                difficulty_pref=data.get("q6"),
            )
            result_obj = RecommendationResult.objects.create(
                user=request.user, 
                preference=pref, 
                ai_reason=ai_reason
            )
            result_obj.books.set([final_book])
        except Exception as e:
            print(f"DB Save Error: {e}")

    # 6. 최종 JSON 응답 생성
    # author_id와 category_id가 ForeignKey인 경우를 고려하여 getattr 사용
    author_obj = getattr(final_book, 'author_id', None)
    category_obj = getattr(final_book, 'category_id', None)

    payload = {
        "ai_reason": ai_reason,
        "books": [
            {
                "id": final_book.id,
                "title": final_book.title,
                "publisher": final_book.publisher,
                "cover_url": final_book.cover_url,
                "author_name": getattr(author_obj, "name", "미상") if author_obj else "미상",
                "category_name": getattr(category_obj, "name", category_name) if category_obj else category_name,
                "reason": temp_reason,
            }
        ],
    }
    
    return Response(payload, status=status.HTTP_200_OK)
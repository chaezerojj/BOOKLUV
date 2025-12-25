import json
from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from klub_talk.models import Book, Category
from .models import ReadingPreference, RecommendationResult
from .services.openai_client import get_ai_recommendation

# 퀴즈 페이지 진입용 (HTML 전용)
def quiz_view(request):
    return render(request, "recommend/quiz.html")

# API 결과 반환용 (JSON 전용)
@api_view(["POST"])
@renderer_classes([JSONRenderer])
def result_view(request):
    # 1. 데이터 수신 (Axios가 보낸 JSON은 request.data에 담김)
    data = request.data
    
    # 2. 장르 매핑 (DB의 Category 이름과 일치하도록 설정)
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
        return Response({"detail": "잘못된 장르 선택입니다."}, status=400)

    # 3. AI 분석용 데이터 정리
    quiz_answers = {
        "목적": data.get("q1"),
        "신간_고전": data.get("q2"),
        "선호_장르": "/".join(category_list),
        "독서스타일": data.get("q8"),
        "분량": data.get("q7"),
        "분위기": data.get("q5"),
        "중요요소": data.get("q6"),
    }

    # 4. DB 도서 조회
    categories = Category.objects.filter(name__in=category_list)
    all_candidate_books = Book.objects.filter(category_id__in=categories)

    if not all_candidate_books.exists():
        return Response({
            "ai_reason": f"'{quiz_answers['선호_장르']}' 장르의 도서를 준비 중입니다.",
            "books": []
        }, status=200)

    # 5. 추천 로직 (기본값 설정 후 AI 업데이트)
    final_book = all_candidate_books.first()
    ai_reason = "분석된 사용자 성향을 바탕으로 추천합니다."
    temp_reason = "이 장르에서 가장 사랑받는 도서 중 하나입니다."

    try:
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
        ai_reason = "AI 추천 과정에서 지연이 발생하여 기본 추천 도서를 제공합니다."

    # 6. 결과 저장 (로그인 유저인 경우)
    if request.user.is_authenticated:
        try:
            pref = ReadingPreference.objects.create(
                user=request.user,
                purpose=quiz_answers["목적"],
                new_vs_classic=quiz_answers["신간_고전"],
                category=quiz_answers["선호_장르"],
                mood=quiz_answers["분위기"],
                reading_style=quiz_answers["독서스타일"],
                length_pref=quiz_answers["분량"],
                difficulty_pref=quiz_answers["중요요소"],
            )
            res_obj = RecommendationResult.objects.create(user=request.user, preference=pref, ai_reason=ai_reason)
            res_obj.books.set([final_book])
        except:
            pass

    # 7. 최종 JSON 응답 (406 에러 해결의 핵심)
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
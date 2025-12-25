import json
from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from klub_talk.models import Book, Category
from .models import ReadingPreference, RecommendationResult
from .services.openai_client import get_ai_recommendation

# 1. 퀴즈 페이지를 보여주는 뷰 (Template 반환)
def quiz_view(request):
    return render(request, "recommend/quiz.html")

# 2. AI 추천 결과를 처리하는 API (JSON 반환)
@api_view(["POST"]) # POST 요청만 처리하도록 제한
@renderer_classes([JSONRenderer])
def result_view(request):
    # 퀴즈 데이터 가져오기 (request.data는 DRF에서 파싱된 JSON 데이터를 담고 있음)
    data = request.data 

    # 장르 매핑 설정
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
        return Response({"detail": "올바른 장르를 선택해주세요."}, status=400)

    # AI 전달용 데이터 구성
    quiz_answers = {
        "목적": data.get("q1"),
        "신간_고전": data.get("q2"),
        "선호_장르": "/".join(category_list),
        "독서스타일": data.get("q8"),
        "분량": data.get("q7"),
        "분위기": data.get("q5"),
        "중요요소": data.get("q6"),
    }

    # DB 조회
    categories = Category.objects.filter(name__in=category_list)
    all_candidate_books = Book.objects.filter(category_id__in=categories)

    if not all_candidate_books.exists():
        return Response({
            "ai_reason": f"죄송합니다. '{quiz_answers['선호_장르']}' 분야의 도서 데이터가 부족합니다.",
            "books": []
        }, status=200)

    # 추천 로직 (AI 호출)
    final_book = all_candidate_books.first()
    ai_reason = "사용자님의 성향을 분석한 결과입니다."
    temp_reason = "추천드리는 도서입니다."

    try:
        # 상위 20권을 AI에게 전달하여 추천 받음
        ai_response = get_ai_recommendation(quiz_answers, all_candidate_books[:20])
        parsed = json.loads(ai_response)
        ai_reason = parsed.get("ai_reason", ai_reason)
        reco_list = parsed.get("recommendations", [])

        if reco_list:
            suggested_id = reco_list[0].get("book_id")
            pick = all_candidate_books.filter(id=suggested_id).first()
            if pick:
                final_book = pick
                temp_reason = reco_list[0].get("reason", temp_reason)
    except Exception as e:
        ai_reason = f"AI 추천 중 오류가 발생했습니다. ({type(e).__name__})"

    # DB 저장 (로그인 사용자)
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
            result_obj = RecommendationResult.objects.create(
                user=request.user, preference=pref, ai_reason=ai_reason
            )
            result_obj.books.set([final_book])
        except Exception as e:
            print(f"DB 저장 오류: {e}")

    # 최종 페이로드 구성
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
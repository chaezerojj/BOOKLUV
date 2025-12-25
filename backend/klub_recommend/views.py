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
    "novel": "소설/시/희곡",
    "essay": "에세이",
    "self_help": "자기계발",
    "humanities": ["인문학", "사회과학"],  # 리스트로 묶음
    "science": "과학",
    "art": "예술/대중문화",
    "economy": "경제경영"
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

    # 1. DB 카테고리 명칭과 퀴즈 선택값 매핑 (DB 데이터 기준)
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
        return Response({"ai_reason": "장르 선택값이 올바르지 않습니다.", "books": []}, status=400)

    # 2. AI 서비스용 딕셔너리 생성 (함수 상단에서 정의)
    quiz_answers = {
        "목적": data.get("q1"),
        "신간_고전": data.get("q2"),
        "선호_장르": "/".join(category_list),
        "독서스타일": data.get("q8"),
        "분량": data.get("q7"),
        "분위기": data.get("q5"),
        "중요요소": data.get("q6"),
    }

    # 3. DB 조회 (PostgreSQL)
    categories = Category.objects.filter(name__in=category_list)
    all_candidate_books = Book.objects.filter(category_id__in=categories)

    # 도서 데이터가 없을 경우 처리
    if not all_candidate_books.exists():
        return Response({
            "ai_reason": f"죄송합니다. '{quiz_answers['선호_장르']}' 장르에 해당하는 도서 데이터가 없습니다.",
            "books": []
        }, status=200)

    # 4. 추천 로직 실행
    final_book = all_candidate_books.first()
    ai_reason = "사용자님의 성향을 분석한 결과입니다."
    reco_data = []

    try:
        # DB의 도서 중 상위 20권을 AI에게 전달
        ai_response = get_ai_recommendation(quiz_answers, all_candidate_books[:20])
        parsed = json.loads(ai_response)
        ai_reason = parsed.get("ai_reason", ai_reason)
        reco_data = parsed.get("recommendations", [])

        if reco_data:
            suggested_id = reco_data[0].get("book_id")
            pick = all_candidate_books.filter(id=suggested_id).first()
            if pick:
                final_book = pick
    except Exception as e:
        ai_reason = f"AI 추천 중 오류가 발생하여 기본 추천 도서를 보여드립니다. ({type(e).__name__})"

    # 5. 추천 사유 설정
    temp_reason = f"{quiz_answers['선호_장르']} 분야에서 인기 있는 도서입니다."
    if reco_data and final_book.id == reco_data[0].get("book_id"):
        temp_reason = reco_data[0].get("reason")

    # 6. DB 저장 (인증된 사용자일 경우)
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
            print(f"DB 저장 실패: {e}")

    # 7. 응답 데이터 구성
    # views.py의 마지막 반환 부분 수정
    context = {
        "ai_reason": ai_reason,  # 템플릿의 {{ ai_reason }}와 매칭
        "results": [             # 템플릿의 {% for book in results %}와 매칭
            {
                "id": final_book.id,
                "title": final_book.title,
                "publisher": final_book.publisher,
                "cover_url": final_book.cover_url,
                "author_id": {"name": getattr(final_book.author_id, "name", "저자 미상")}, # .author_id.name 구조 대응
                "category_id": {"name": getattr(final_book.category_id, "name", "장르 미상")}, # .category_id.name 구조 대응
                "temp_reason": temp_reason, # 템플릿의 {{ book.temp_reason }}와 매칭
            }
        ],
    }

    return render(request, "recommend/result.html", context)
    # return Response(payload, status=status.HTTP_200_OK)
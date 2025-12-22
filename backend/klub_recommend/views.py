import json
from django.shortcuts import render
from rest_framework.decorators import api_view
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
    if request.method != "POST":
        return render(request, "recommend/quiz.html")

    # 🔹 1. 퀴즈 응답 수집
    quiz_answers = {
        "목적": request.POST.get("q1"),
        "신간_고전": request.POST.get("q2"),
        "선호_장르": request.POST.get("q4"),
        "분량": request.POST.get("q7"),
        "독서스타일": request.POST.get("q8"),
        "필요한책": request.POST.get("q10"),
    }

    # 🔹 2. 카테고리 필터링 및 후보군 추출
    category_name = GENRE_MAP.get(request.POST.get("q4"))
    quiz_answers["선호_장르_이름"] = category_name # 프롬프트용 이름 저장
    
    categories = Category.objects.filter(name=category_name)
    # 원본 쿼리셋 (슬라이싱 전) - 여기서 필터링해야 에러가 안 납니다.
    all_candidate_books = Book.objects.filter(category_id__in=categories)

    if not all_candidate_books.exists():
        return render(request, "recommend/result.html", {"results": [], "ai_reason": "현재 추천 가능한 도서가 없습니다."})

    # AI에게 보낼 후보군 (상위 20권)
    books_for_ai = all_candidate_books[:20]

    # 🔹 3. GPT 추천 요청
    ai_response = get_ai_recommendation(quiz_answers, books_for_ai)
    parsed = json.loads(ai_response)
    
    ai_reason = parsed.get("ai_reason", "사용자님의 성향을 분석한 결과입니다.")
    reco_data = parsed.get("recommendations", [])
    
    # 🔹 4. AI가 추천한 첫 번째 book_id 검증
    suggested_id = reco_data[0].get("book_id") if reco_data else None
    
    # ⚠️ 핵심 수정: 슬라이싱 에러 방지를 위해 .first() 대신 필터링 후 리스트로 변환하여 추출
    recommended_book_qs = all_candidate_books.filter(id=suggested_id).select_related('author_id', 'category_id')

    if recommended_book_qs.exists():
        final_book = recommended_book_qs[0] # 인덱싱 사용
    else:
        # AI가 준 ID가 없으면 후보군 중 첫 번째 책을 리스트로 변환해 가져옴
        final_book = list(all_candidate_books[:1])[0]

    # 🔹 5. DB 저장 로직
    user = request.user if request.user.is_authenticated else User.objects.first()
    
    pref = ReadingPreference.objects.create(
        user=user,
        purpose=quiz_answers["목적"],
        new_vs_classic=quiz_answers["신간_고전"],
        category=quiz_answers["선호_장르"],
        mood=request.POST.get("q5"),
        reading_style=quiz_answers["독서스타일"],
        length_pref=quiz_answers["분량"],
        difficulty_pref=request.POST.get("q6"),
    )

    result_obj = RecommendationResult.objects.create(
        user=user, preference=pref, ai_reason=ai_reason
    )
    result_obj.books.set([final_book])

    # 🔹 6. 템플릿용 개별 코멘트 매핑
    # AI가 보낸 구체적인 추천 코멘트(reason)를 객체에 주입
    if reco_data and final_book.id == reco_data[0].get("book_id"):
        final_book.temp_reason = reco_data[0].get("reason")
    else:
        # AI 응답 실패 시 사용자 요청 양식에 맞춘 기본 문구
        final_book.temp_reason = (
            f"사용자님이 선호하시는 장르는 {category_name}입니다. "
            f"이 책은 사용자의 취향을 반영한 깊이 있는 이야기를 담고 있습니다. "
            f"새로운 영감이 필요하다면 오늘 '{final_book.title}'은 어떠실까요?"
        )

    return render(request, "recommend/result.html", {
        "results": [final_book], # 1권만 리스트로 감싸서 전달
        "ai_reason": ai_reason
    })
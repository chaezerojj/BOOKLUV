def build_recommend_prompt(quiz_answers, books):
    # 1. 도서 리스트 생성 시 방어적 속성 접근
    book_details = []
    for b in books:
        author = getattr(b.author_id, 'name', '미상') if b.author_id else '미상'
        category = getattr(b.category_id, 'name', '기타') if b.category_id else '기타'
        desc = (b.description[:100] + '...') if b.description else "상세 설명 없음"
        
        book_details.append(
            f"ID: {b.id} | 제목: {b.title} | 작가: {author} | 장르: {category} | 주제: {desc}"
        )
    
    book_list_str = "\n".join(book_details)

    system_message = {
        "role": "system",
        "content": (
            "너는 독서 성향 분석 전문가이자 친절한 도서 큐레이터다. "
            "반드시 제공된 JSON 형식으로만 응답하며, 모든 필드를 엄격히 채워라."
        ),
    }

    user_message = {
        "role": "user",
        "content": f"""
[사용자 데이터]
- 선호 장르: {quiz_answers.get('선호_장르_이름', '미지정')}
- 독서 목적: {quiz_answers.get('목적', '독서')}
- 선호 분위기: {quiz_answers.get('mood', '편안한')}

[도서 목록]
{book_list_str}

위 목록 중 사용자 성향에 가장 적합한 '1권'을 선정하여 아래 JSON 형식으로 응답해라. 
'reason'은 반드시 제공된 예시의 문장 구조를 100% 준수하여 3~4줄로 작성해라.

[추천 코멘트 필수 문장 구조]
1. "사용자님이 선호하시는 장르는 (장르명) 입니다."
2. "이 책은 (주제/내용)를 주제로 쓰여진 책으로, (분야/특징)에서 인기를 얻고 있는 책입니다."
3. "(어떤 점)이 좋다면, 오늘은 (제목)은 어떠실까요?"

[응답 JSON 형식]
{{
  "ai_reason": "사용자 성향에 대한 전체적인 분석 요약",
  "recommendations": [
    {{
      "book_id": 실제 숫자 ID,
      "reason": "필수 문장 구조를 포함한 3~4줄의 코멘트"
    }}
  ]
}}

※ 주의: JSON 이외의 설명이나 인사말은 생략할 것.
"""
    }
    return [system_message, user_message]
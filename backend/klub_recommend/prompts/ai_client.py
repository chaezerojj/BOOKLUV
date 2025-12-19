def build_recommend_prompt(quiz_answers, books):
    # AI가 참고할 책 상세 리스트 생성
    book_list_str = "\n".join([
        f"ID: {b.id} | 제목: {b.title} | 작가: {b.author_id.name if b.author_id else '미상'} | 장르: {b.category_id.name} | 주제: {b.description[:100]}" 
        for b in books
    ])

    system_message = {
        "role": "system",
        "content": (
            "너는 독서 성향 분석 전문가이자 친절한 도서 큐레이터다. "
            "사용자의 성향(목적, 장르, 분위기)을 분석하여 맞춤형 코멘트를 작성해야 한다."
        ),
    }

    user_message = {
        "role": "user",
        "content": f"""
[사용자 데이터]
- 선호 장르: {quiz_answers.get('선호_장르_이름', '선택한 장르')}
- 독서 목적: {quiz_answers.get('목적')}
- 선호 분위기: {quiz_answers.get('mood')}

[도서 목록]
{book_list_str}

위 목록 중 딱 '1권'만 엄선해서 아래 JSON 형식으로 응답해라. 
'reason'은 반드시 다음 문장 구조를 포함해 3~4줄로 작성해라:
'ai_reason'은 전체적인 분석을 적고, 'recommendations' 내부의 'reason'은 각 책마다 아래의 문장 구조를 활용해 3~4줄로 작성해라.

[추천 코멘트 필수 포함 내용]
1. "사용자님이 선호하시는 장르는 (장르명) 입니다."로 시작할 것.
2. "이 책은 (주제/내용)를 주제로 쓰여진 책으로, (분야/특징)에서 인기를 얻고 있는 책입니다." 포함.
3. "(어떤 점)이 좋다면, 오늘은 (제목)은 어떠실까요?"라는 권유형 문장으로 마무리.
4. 위의 추천 코멘트를 작성할 때, 추천 도서의 상세 설명과 제목을 참고하여 작성할 것.

[예시1]
 사용자님이 선호하시는 장르는 자기계발서/실용서입니다. 
 이 책은 저축과 저소비를 주제로 쓰여진 책으로, 자기계발서 분야에서 인기를 얻고 있습니다.
 소비에 대한 책이 읽고 싶다면, 오늘은 커피 한 잔과 함께 <저소비 생활>은 어떠실까요?

[예시2]
 사용자님이 선호하시는 장르는 소설/에세이입니다. 
 이 책은 최근 발행된 소설로, 구병모 작가가 저술한 신간 장편 소설입니다.
 길어도 완성도가 있는 소설을 원하신다면, 이번 주말은 <절창>과 함께 보내는 건 어떠세요?


{{
  "ai_reason": "사용자의 전반적인 독서 성향 분석 결과...",
  "recommendations": [
    {{
      "book_id": 실제ID,
      "reason": "사용자님이 선호하시는 장르는... (위 지시사항 대로 3~4줄 작성)"
    }}
  ]
}}
"""
    }
    return [system_message, user_message]
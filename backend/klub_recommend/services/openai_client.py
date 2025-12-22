# klub_recommend/services/openai_client.py
import os
import requests

GMS_API_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions"
GMS_KEY = os.getenv("GMS_KEY")

def get_ai_recommendation(quiz_answers, books):
    """
    quiz_answers: dict
    books: QuerySet[Book]
    """

    book_list_text = "\n".join([
        f"- {book.id}. {book.title}: {book.description[:100]}"
        for book in books
    ])

    prompt = f"""
사용자의 독서 취향 퀴즈 응답은 다음과 같다:
{quiz_answers}

아래는 추천 후보 도서 목록이다:
{book_list_text}

조건:
- 위 도서 중에서만 추천할 것
- 1권 추천
- 각 책마다 '추천 이유'를 2문장 이내로 작성
- JSON 형식으로만 응답

응답 형식:
{{
  "recommendations": [
    {{
      "book_id": 1,
      "reason": "추천 이유"
    }}
  ]
}}
"""

    response = requests.post(
        GMS_API_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GMS_KEY}",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a book recommendation assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

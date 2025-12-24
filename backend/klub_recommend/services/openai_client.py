# klub_recommend/services/openai_client.py
import os
import json
import requests

GMS_API_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions"

def get_ai_recommendation(quiz_answers, books):
    gms_key = os.getenv("GMS_KEY")
    if not gms_key:
        # 배포에서 키 없으면 여기서 명확히 터뜨려서 원인 바로 보이게
        raise RuntimeError("GMS_KEY is missing in environment variables")

    book_list_text = "\n".join([
        f"- {book.id}. {book.title}: {(book.description or '')[:100]}"
        for book in books
    ])

    prompt = f"""
사용자의 독서 취향 퀴즈 응답:
{quiz_answers}

추천 후보 도서 목록(이 목록에서만 선택):
{book_list_text}

반드시 아래 JSON만 출력:
{{
  "ai_reason": "성향 분석 요약(1~2문장)",
  "recommendations": [
    {{
      "book_id": 1,
      "reason": "추천 이유(2문장 이내)"
    }}
  ]
}}
"""

    res = requests.post(
        GMS_API_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {gms_key}",
        },
        json={
            "model": "gpt-4o-mini",
            # JSON 모드 강제 지정
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": "You are a book recommendation assistant."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        },
        timeout=30,
    )

    # 실패 시 본문을 같이 보여주면 배포 로그에서 원인 파악 쉬움
    if res.status_code != 200:
        raise RuntimeError(f"GMS API failed: {res.status_code} {res.text[:300]}")

    content = res.json()["choices"][0]["message"]["content"]

    # JSON 모드여도 방어적으로 한 번 더 검사
    try:
        json.loads(content)
    except Exception:
        raise RuntimeError(f"Model did not return valid JSON: {content[:300]}")

    return content

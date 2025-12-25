# klub_recommend/services/openai_client.py
import os
import json
import requests

GMS_API_URL = "https://gms.ssafy.io/gmsapi/api.openai.com/v1/chat/completions"

def get_ai_recommendation(quiz_answers, books):
    gms_key = os.getenv("GMS_KEY")
    if not gms_key:
        raise RuntimeError("GMS_KEY is missing in environment variables")

    # 책 목록을 문자열로 변환
    book_list_text = "\n".join([
        f"- {book.id}. {book.title}: {(book.description or '')[:100]}"
        for book in books
    ])

    prompt = f"""
사용자의 독서 취향 퀴즈 응답:
{quiz_answers}

추천 후보 도서 목록 (이 목록에 있는 도서의 ID만 사용):
{book_list_text}

[지침]
1. 사용자의 응답을 분석하여 가장 잘 어울리는 도서를 후보 목록에서 **반드시 1권** 선택하세요.
2. 만약 후보 목록 중 사용자의 취향에 완벽히 부합하는 책이 없다면, 목록에 있는 도서 중 가장 대중적이거나 흥미로운 도서를 **임의로라도 반드시 1권 선택**해야 합니다.
3. 절대 "추천할 도서가 없다"는 응답을 하지 마세요.

반드시 아래 JSON 형식으로만 응답하세요:
{{
  "ai_reason": "사용자의 성향(목적, 스타일 등)을 기반으로 한 전체적인 분석 요약 (1~2문장)",
  "recommendations": [
    {{
      "book_id": 실제 도서의 ID 숫자,
      "reason": "해당 도서를 추천하는 구체적인 이유 (2문장 이내)"
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

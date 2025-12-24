# klub_recommend/services/reason_generator.py
def build_reason_text(pref, books):
    titles = ", ".join([b.title for b in books])

    return f"""
당신은 지금 '{pref.purpose}'을(를) 목적으로 책을 찾고 있으며,
'{pref.category}' 분야에서 '{pref.mood}'한 분위기의 책을 선호합니다.

아래 책들은 그런 취향에 잘 맞습니다:
{titles}

특히 지금의 독서 스타일과 분량 선호를 고려해
부담 없이 시작할 수 있는 책들로 골랐어요.
"""

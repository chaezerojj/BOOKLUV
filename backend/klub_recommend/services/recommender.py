from klub_talk.models import Book, Category

def recommend_books(quiz_answers: dict):
    """
    quiz_answers 예:
    {
        "q1": "novel",
        "q2": "humanities",
        "q3": "novel"
    }
    """

    score = {}

    for answer in quiz_answers.values():
        score[answer] = score.get(answer, 0) + 1

    # 가장 많이 나온 카테고리
    top_category_key = max(score, key=score.get)

    category_map = {
        "humanities": "인문학",
        "novel": "소설/시/희곡",
        "social": "사회과학",
        "economy": "경제경영",
        "essay": "에세이",
        "science": "과학",
        "art": "예술/대중문화",
        "self": "자기계발",
    }

    category_name = category_map[top_category_key]

    category = Category.objects.get(name=category_name)
    books = Book.objects.filter(category_id=category)[:5]

    return category_name, books

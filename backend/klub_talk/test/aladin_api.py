import requests
import json

API_KEY = "ttbzziruregi1043001"  # 여기에 TTBKey 입력
URL = "http://www.aladin.co.kr/ttb/api/ItemList.aspx"

params = {
    "ttbkey": API_KEY,
    "QueryType": "Bestseller",
    "MaxResults": 50,
    "Start": 1,
    "SearchTarget": "Book",
    "Output": "JS",
    "Cover": "Big",
    "Version": 20131101
}

response = requests.get(URL, params=params)
text = response.text
if text.startswith("callback("):
    text = text[len("callback("):-2]

data = json.loads(text)
items = data.get("item", [])

# 중복 제거용 세트
category_set = set()
author_set = set()

# 카테고리, 저자, 책 fixture 생성
categories = []
authors = []
books = []

category_map = {}  # 카테고리 이름 -> PK
author_map = {}    # 저자 이름 -> PK

cat_pk = 1
auth_pk = 1

for item in items:
    # Category 처리 (중분류만 사용)
    raw_category = item.get("categoryName", "")
    # '>' 기준으로 분리하고 두 번째 요소(중분류)만 사용
    cat_name = "기타"
    if raw_category:
        parts = raw_category.split(">")
        if len(parts) > 1:
            cat_name = parts[1].strip()
        else:
            cat_name = parts[0].strip()

    if cat_name not in category_set:
        category_set.add(cat_name)
        category_map[cat_name] = cat_pk
        categories.append({
            "model": "klub_talk.category",
            "pk": cat_pk,
            "fields": {"name": cat_name}
        })
        cat_pk += 1

    # Author 처리 (지은이만)
    raw_author = item.get("author", "미상")
    # '(', ')'를 기준으로 지은이만 추출
    if "(" in raw_author:
        raw_author = raw_author.split("(")[0].strip()

    auth_name = raw_author
    if auth_name not in author_set:
        author_set.add(auth_name)
        author_map[auth_name] = auth_pk
        authors.append({
            "model": "klub_talk.author",
            "pk": auth_pk,
            "fields": {"name": auth_name}
        })
        auth_pk += 1

    # Book 생성
    books.append({
        "model": "klub_talk.book",
        "fields": {
            "aladin_id": item.get("itemId"),
            "title": item.get("title"),
            "author_id": author_map[auth_name],
            "publisher": item.get("publisher", ""),
            "category_id": category_map[cat_name],
            "pub_date": item.get("pubDate") or None,
            "cover_url": item.get("cover", ""),
            "description": item.get("description", "")
        }
    })

# JSON 저장
with open("categories.json", "w", encoding="utf-8") as f:
    json.dump(categories, f, ensure_ascii=False, indent=4)
with open("authors.json", "w", encoding="utf-8") as f:
    json.dump(authors, f, ensure_ascii=False, indent=4)
with open("books.json", "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=4)

print("categories.json, authors.json, books.json 생성 완료!")

import requests
import json

API_KEY = ""
URL = f"http://www.aladin.co.kr/ttb/api/ItemList.aspx"
params = {
    "ttbkey": API_KEY,
    "QueryType": "Bestseller",
    "MaxResults": 50,
    "Start": 1,
    "SearchTarget": "Book",
    "Output": "JS",  # JS/JSON 형식
    "Cover": "Big",
    "Version": 20131101
}

response = requests.get(URL, params=params)
print(response.status_code)
print(response.text[:500])  # 실제 반환 내용 확인

# JSON 변환 (JS 형식이면 callback 제거 필요할 수 있음)
text = response.text
if text.startswith("callback("):
    text = text[len("callback("):-2]  # 마지막 ');' 제거

data = json.loads(text)
items = data.get("item", [])

# fixture 생성
fixtures = []
for i, item in enumerate(items, start=1):
    fixtures.append({
        "model": "klub_talk.book",
        "fields": {
            "aladin_id": item.get("itemId"),
            "title": item.get("title"),
            "author": item.get("author"),
            "publisher": item.get("publisher"),
            "pub_date": item.get("pubDate") or None,
            "cover_url": item.get("cover"),
            "description": item.get("description", "")
        }
    })

with open("books.json", "w", encoding="utf-8") as f:
    json.dump(fixtures, f, ensure_ascii=False, indent=4)

print("books.json 생성 완료!")

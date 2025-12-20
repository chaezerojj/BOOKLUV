from django.shortcuts import render, get_object_or_404
from .models import Meeting, Book, Participate, Quiz
from klub_user.models import User
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BookSerializer

def index(request):
    return render(request, 'talk/index.html')

# 알라딘 api 테스트
def aladin_api(request):
    books = Book.objects.all()
    return render(request, 'talk/book_list.html', {'books': books})

# 책 목록
def book_list(request):
    search_query = request.GET.get('q', '')  # 검색어
    type_filter = request.GET.get('type', 'book')  # 검색 타입, 기본값은 'book'

    books = Book.objects.all()  # 기본값으로 모든 책을 가져옵니다.

    if search_query:
        # 책 제목, 작가명, 장르명, 설명으로 검색
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author_id__name__icontains=search_query) |
            Q(category_id__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    return render(request, 'talk/book_list.html', {'books': books, 'type_filter': type_filter})

 # 책 상세 정보
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    meetings = Meeting.objects.filter(book_id=book) 
    return render(request, 'talk/book_detail.html', {
        'book': book,
        'meetings': meetings,
    })
    
def room_detail(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)
    print(meeting)
    # 조회수 증가
    meeting.views += 1
    meeting.save(update_fields=['views'])
    return render(request, 'talk/room_detail.html', {'meeting': meeting})


def quiz_view(request, meeting_id):
    quiz = get_object_or_404(Quiz, meeting_id=meeting_id)
    meeting = quiz.meeting_id

    if request.method == "POST":
        user_answer = request.POST.get("answer")
        result = (user_answer.strip() == quiz.answer.strip())

        Participate.objects.update_or_create(
            meeting_id=meeting,
            user_id=User.objects.get(pk=1),  # 나중에 request.user로 교체
            defaults={"result": result}
        )

        return render(request, "talk/quiz_result.html", {
            "quiz": quiz,
            "result": result,
            "meeting": meeting
        })

    # GET 요청 처리: quiz.html 템플릿을 렌더
    return render(request, "talk/quiz.html", {"quiz": quiz, "meeting": meeting})


@api_view(['GET'])
def book_search_api(request):
    q = (request.GET.get('q') or '').strip()
    books = Book.objects.all()
    
    if q:
        books = books.filter(
            Q(title__icontains=q) |
            Q(author_id__name__icontains=q) |
            Q(category_id__name__icontains=q) |
            Q(description__icontains=q)
        )
    
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Meeting, Book, Participate, Quiz
from klub_user.models import User
from django.db.models import Q, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .forms import MeetingForm, QuizForm
from .serializers import BookSerializer, MeetingDetailSerializer, MeetingMiniSerializer, QuizSerializer

@api_view(["GET"])
def index(request):
    return render(request, 'talk/index.html')

# 알라딘 api 테스트
@api_view(["GET"])
def aladin_api(request):
    books = Book.objects.all()
    return render(request, 'talk/book_list.html', {'books': books})

# 책 목록
@api_view(["GET"])
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
@api_view(["GET"])
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    meetings = Meeting.objects.filter(book_id=book) 
    return render(request, 'talk/book_detail.html', {
        'book': book,
        'meetings': meetings,
    })
    
@api_view(["GET"])
def room_detail(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk)

    # 조회수 증가
    meeting.views += 1
    meeting.save(update_fields=['views'])

    # 참여 인원 계산
    joined_count = Participate.objects.filter(meeting=meeting, result=True).count()

    participated = False
    can_participate = True
    remaining_chances = 3  # 기본 참여 기회

    if request.user.is_authenticated:
        # 이미 참여 완료했는지
        participated = Participate.objects.filter(
            meeting=meeting,
            user_id=request.user,
            result=True
        ).exists()

        # 틀린 횟수 체크
        wrong_count = Participate.objects.filter(
            meeting=meeting,
            user_id=request.user,
            result=False
        ).count()
        remaining_chances = max(0, 3 - wrong_count)

        if remaining_chances == 0:
            can_participate = False

    return render(request, 'talk/room_detail.html', {
        'meeting': meeting,
        'joined_count': joined_count,
        'participated': participated,
        'can_participate': can_participate,
        'remaining_chances': remaining_chances
    })


@api_view(["GET", "POST"])
def quiz_view(request, meeting_id):
    quiz = get_object_or_404(Quiz, meeting_id=meeting_id)
    meeting = quiz.meeting_id  # Meeting 객체

    user = request.user  # 현재 로그인 유저

    # 이미 틀린 횟수
    wrong_count = Participate.objects.filter(
        meeting=meeting,
        user_id=user,
        result=False
    ).count()
    remaining_chances = max(0, 3 - wrong_count)

    result = None  # 기본값

    if request.method == "POST":
        user_answer = request.POST.get("answer", "").strip()
        correct_answer = quiz.answer.strip()
        result = (user_answer == correct_answer)

        # 틀리면 result=False 레코드 생성
        Participate.objects.create(
            meeting=meeting,
            user_id=user,
            result=result
        )

        # 남은 기회 업데이트 (틀린 경우)
        if not result:
            wrong_count += 1
            remaining_chances = max(0, 3 - wrong_count)

        return render(request, "talk/quiz_result.html", {
            "quiz": quiz,
            "result": result,
            "meeting": meeting,
            "remaining_chances": remaining_chances
        })

    return render(request, "talk/quiz.html", {
        "quiz": quiz,
        "meeting": meeting,
        "remaining_chances": remaining_chances
    })

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

@api_view(['GET'])
def book_detail_api(request, book_id):
    book = Book.objects.get(pk=book_id)
    # 이 책으로 개설된 모임들
    meetings = Meeting.objects.filter(book_id=book).order_by('-created_at') 
    data = {
        "book": BookSerializer(book).data,
        "meetings": MeetingMiniSerializer(meetings, many=True).data,
    }
    return Response(data)


@api_view(['GET'])
def meeting_detail_api(request, pk):
    meeting = Meeting.objects.get(pk=pk)
    return Response(MeetingDetailSerializer(meeting).data)


@api_view(['GET', 'POST'])
def quiz_api(request, meeting_id):
    quiz = Quiz.objects.get(meeting_id=meeting_id)

    if request.method == 'GET':
        return Response(QuizSerializer(quiz).data)

    # POST: 채점
    user_answer = (request.data.get('answer') or '').strip()
    correct = (quiz.answer or '').strip()

    result = (user_answer == correct)

    return Response({
        "question": quiz.question,
        "user_answer": user_answer,
        "answer": correct,
        "result": result,
    }, status=status.HTTP_200_OK)

def meeting_search(request):
    query = request.GET.get("q", "")

    # 모임 queryset 준비
    meetings = Meeting.objects.select_related("book_id", "leader_id")

    # joined_count 계산
    meetings = meetings.annotate(
        joined_count=Count(
            "participations",
            filter=Q(participations__result=True)
        )
    ).order_by("-created_at")

    # 검색어가 있으면 필터링
    if query:
        meetings = meetings.filter(
            Q(title__icontains=query) |
            Q(book_id__title__icontains=query)
        )

    return render(request, "talk/meeting_list.html", {
        "meetings": meetings,
        "query": query,
        "is_search": True,
    })
    

def create_meeting(request, pk):
    book = Book.objects.get(id=pk)
    
    if request.method == 'POST':
        meeting_form = MeetingForm(request.POST)
        quiz_form = QuizForm(request.POST)

        if meeting_form.is_valid() and quiz_form.is_valid():
            meeting = meeting_form.save(commit=False)
            meeting.book_id = book
            meeting.leader_id = request.user
            meeting.save()

            quiz = quiz_form.save(commit=False)
            quiz.meeting_id = meeting
            quiz.save()

            return redirect('talk:book-detail', book_id=book.id)  # 생성 후 리다이렉트
    else:
        meeting_form = MeetingForm()
        quiz_form = QuizForm()

    return render(request, 'talk/create_meeting.html', {
        'book': book,
        'meeting_form': meeting_form,
        'quiz_form': quiz_form,
    })
    
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# @login_required
# @require_POST
def cancel_participation(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)

    # result=True인 Participate 레코드 삭제
    Participate.objects.filter(
        meeting=meeting,
        user_id=request.user,
        result=True
    ).delete()

    # 삭제 후 모임 상세 페이지로 리다이렉트
    return redirect('talk:meeting-test-detail', pk=meeting_id)

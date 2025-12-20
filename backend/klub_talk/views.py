from django.db import models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from .models import Meeting, Book, Participate, Quiz
from klub_user.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import QuizForm

def index(request):
    return render(request, 'talk/index.html')

# 알라딘 api 테스트
def aladin_api(request):
    books = Book.objects.all()
    return render(request, 'talk/book_list.html', {'books': books})

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


# @login_required
def quiz_view(request, meeting_id):
    quiz = get_object_or_404(Quiz, meeting_id=meeting_id)
    meeting = quiz.meeting_id

    if request.method == "POST":
        user_answer = request.POST.get("answer")
        result = (user_answer.strip() == quiz.answer.strip())

        # 참여 정보 생성
        Participate.objects.update_or_create(
            meeting_id=meeting,
            user_id= User.objects.get(pk=1) ,#request.user,
            defaults={"result": result}
        )

        return render(request, "talk/quiz_result.html", {
            "quiz": quiz,
            "result": result,
            "meeting": meeting
        })

    return render(request, "talk/quiz.html", {"quiz": quiz, "meeting": meeting})


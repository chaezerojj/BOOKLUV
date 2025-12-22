from django.shortcuts import render, redirect

# 현재 디렉토리의 models.py로 부터 Board 모델을 가져오겠다. 
from .models import Board, Comment

from .forms import BoardForm, CommentForm

from django.contrib.auth.decorators import login_required

def index(request):
    # QuerySetAPI ---> Read, 전체 데이터 조회 : Board.objects.all()
    boards = Board.objects.all()
    print(boards)

    context = {
        'boards' : boards,
    }

    return render(request, 'board/index.html', context)

def detail(request, pk):
    # QuerySet API : 단일 데이터 조회 : get
    board = Board.objects.get(pk=pk)

    comment_form = CommentForm()
    # 게시글에 있는 댓글을 모두 가져온다 (역참조)
    comments = board.comment_set.all()

    context = {
        'board': board,
        'comment_form': comment_form,
        'comments': comments
    }

    return render(request, 'board/detail.html', context)


def comments_create(request, pk):
    # 유효성 검사 전
    board = Board.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    # 댓글 유효성 검사
    if comment_form.is_valid():
        # 유효성 검사 하고 바로 DB에 저장?? X
        # commit = False : 바로 저장하지 않고 추가 작업 후 저장
        comment = comment_form.save(commit=False)
        comment.board = board # 1. 게시글의 객체 (참조)
        comment.user = request.user # 2. 현재 로그인한 사용자
        comment.save() # DB에 수동으로 저장
        return redirect('board:detail', board.pk)
    # 유효성 검사 실패했을때
    context = {
        'board': board,
        'comment_form': comment_form
    }
    return render(request, 'board/detail.html', context)


def comments_delete(request, board_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    # 현재 로그인 유저 == 댓글 작성한 유저
    if request.user == comment.user:
        comment.delete()
    return redirect('board:detail', board_pk)

@login_required(login_url='/api/v1/auth/')
def create(request):
    # GET 방식 : url에 노출 --- 데이터 조회, 검색
    # POST 방식 : url에 노출 x(보안성) --- 데이터 생성, 수정, 삭제
    # POST방식이 짱이지만 GET방식을 쓰는 이유
    # GET방식에 비해 POST방식 훨씬 복잡하다. : ex) (csrf토큰) - (보안토큰)
    
    # 내가(클라이언트가) 게시글 생성 버튼(submit버튼)을 눌렀을 때
    if request.method == 'POST':
        # request.POST : 클라이언트가 POST방식으로 전송한 폼데이터
        # request.FILES : 클라이언트가 업로드한 모든 파일
        form = BoardForm(request.POST, request.FILES)
        # 유효성 검사
        if form.is_valid(): # 유효성 검사에 성공
            # commit=False : 중간 단계를 거치고 수동으로 저장
            board = form.save(commit=False) # DB에 자동 저장
            # request.user : 로그인한 사용자
            board.user = request.user
            # DB에 저장
            board.save()
            # 데이터가 변경 되었기 때문에 redirect
            return redirect('board:detail', board.pk)

    # 버튼 누르기 전에 or 다른 버튼을 눌렀을떄(다른 method)
    else:
        form = BoardForm()
    # GET요청일때(+실패 했을 때)
    # 빈 폼
    context = {
        'form' : form
    }
    return render(request, 'board/create.html', context)


# 단일 게시글 조회 후 삭제
def delete(request, pk):
    # QuerySetAPI
    board = Board.objects.get(pk=pk)
    board.delete()

    return redirect('board:index')


# 페이지 렌더링 + 리다이렉트(create와 차이 : 기존에 있던 게시글을 변경)
def update(request, pk):
    board = Board.objects.get(pk=pk)

    # submit 버튼 눌렀을떄
    if request.method == 'POST':
        # 기존 게시글의 데이터(instanc=article)
        form = BoardForm(request.POST, request.FILES, instance=board)
        # 유효성 검사
        if form.is_valid():
            form.save() # 유효성 검사 성공하면 DB에 저장
            # 데이터 변경 되었으니 redirect
            return redirect('board:detail', board.pk)
    # submit 버튼을 누르기전 or 다른버튼 눌렀을 때
    else:
        # 기존의 게시글의 글
        form = BoardForm(instance=board)
    # GET요청 일때
    context = {
        'board' : board,
        'form' : form
    }
    # 데이터 변경이 x
    return render(request, 'board/update.html', context)
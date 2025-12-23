from django import forms
from .models import Board, Comment

# form 태그와 django model form 차이
# model form 왜쓸까??

# form 태그는 name으로 넘겨주고 views.py에서 DB저장
# model form은 바로 db에 저장
# 편해서(유효성검사도 쉽게)

class BoardForm(forms.ModelForm):
    # class Meta : 폼의 기본 구조를 자동으로 생성
    # 위젯으로 세부 조정 가능
    class Meta:
        model = Board
        # fields = ('title', 'content', 'create_at', 'updated_at', )
        # fields = '__all__'
        fields = (
            'title',
            'content',
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
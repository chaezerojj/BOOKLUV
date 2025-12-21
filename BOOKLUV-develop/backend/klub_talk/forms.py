from django import forms

class QuizForm(forms.Form):
    answer = forms.CharField(label='퀴즈 답안', max_length=100)
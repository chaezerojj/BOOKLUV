# forms.py
from django import forms
from .models import Meeting, Quiz
from django.utils import timezone

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'description', 'members', 'started_at', 'finished_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 50}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'maxlength': 200}),
            'members': forms.NumberInput(attrs={'class': 'form-control', 'min': 2, 'max': 20}),
            'started_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'finished_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        started_at = cleaned_data.get('started_at')
        finished_at = cleaned_data.get('finished_at')

        if started_at and started_at < timezone.now():
            self.add_error('started_at', '시작 시간은 현재보다 과거일 수 없습니다.')

        if started_at and finished_at and finished_at <= started_at:
            self.add_error('finished_at', '종료 시간은 시작 시간보다 늦어야 합니다.')

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['question', 'answer']

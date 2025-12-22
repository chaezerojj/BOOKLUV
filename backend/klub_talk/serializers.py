from rest_framework import serializers
from .models import Book, Meeting, Quiz

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author_id.name', read_only=True, default=None)
    category_name = serializers.CharField(source='category_id.name', read_only=True, default=None)

    class Meta:
        model = Book
        fields = [
            'id',
            'aladin_id',
            'title',
            'author_name',
            'category_name',
            'publisher',
            'pub_date',
            'cover_url',
            'description',
        ]

class MeetingMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = [
            'id', 
            'title', 
            'members', 
            'views', 
            'description', 
            'started_at', 
            'finished_at'
            ]

class MeetingDetailSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book_id.title', read_only=True, default=None)
    leader_name = serializers.CharField(source='leader_id.username', read_only=True, default=None)

    class Meta:
        model = Meeting
        fields = [
            'id', 'title',
            'book_title',
            'leader_name',
            'members', 'views',
            'description',
            'started_at', 'finished_at',
        ]

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'question']
from rest_framework import serializers
from .models import Book

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

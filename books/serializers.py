from rest_framework import serializers
from .models import Book,Category, Review

class BookSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'author', 'ISBN', 'category','publication_date', 'created_at', 'updated_at', 'average_rating', 'borrower_count']


    def get_average_rating(self, obj):
        return obj.average_rating()

class ReviewSerializer(serializers.ModelSerializer):
    borrower_name = serializers.CharField(source='borrower.user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'borrower', 'borrower_name', 'book', 'book_title', 'rating', 'comment', 'created_at']
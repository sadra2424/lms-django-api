from rest_framework import viewsets, status
from rest_framework import filters
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated
from borrowers.permissions import IsAdminUser, IsBorrowerUser


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author__name', 'category__name']
    filterset_fields = ['category', 'language', 'availability']

class ReviewViewSet(viewsets.ModelViewSet):
    from .serializers import ReviewSerializer
    from .models import Review
    from rest_framework.response import Response
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsBorrowerUser]

    def create(self, request, *args, **kwargs):
        borrower = request.data.get("borrower")
        book = request.data.get("book")
        if Review.objects.filter(borrower=borrower, book=book).exists():
            return Response({"error": "You have already reviewed this book"}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
        
from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import BorrowingTransaction, Reservation
from .serializers import BorrowingTransactionSerializer, ReservationSerializer
from django.utils import timezone
from books.models import Book
from rest_framework.response import Response
from rest_framework import status


class BorrowingTransactionViewSet(viewsets.ModelViewSet):
    queryset = BorrowingTransaction.objects.all()
    serializer_class = BorrowingTransactionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['borrower__user__username', 'book__title']

    def create(self, request, *args, **kwargs):
        borrower = request.data.get("borrower")
        if BorrowingTransaction.objects.filter(borrower=borrower, return_date__isnull=True).count() >=5:
             return Response({"error": "You have reached the maximum number of borrowed books."}, status=status.HTTP_400_BAD_REQUEST)
        #دریافت داده ها برای افزایش تعداد امانت گیری های یک کتاب
        book_id = request.data.get("book")
        book = Book.objects.get(id=book_id)

        book.borrower_count += 1
        book.save()

        return super().create(request, *args, **kwargs)

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    
    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book")
        borrower_id = request.data.get("borrower")

        if BorrowingTransaction.objects.filter(book_id=book_id, return_date__isnull=True).exists():
            if Reservation.objects.filter(book_id=book_id, borrower_id=borrower_id, is_active=True).exists():
                return Response({"error": "You have already reserved this book."}, status=status.HTTP_400_BAD_REQUEST)
            return super().create(request, *args, **kwargs)
        else:
            return Response({"error": "This book is currently unavailable for borrowing."}, status=status.HTTP_400_BAD_REQUEST)
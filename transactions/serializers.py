from rest_framework import serializers
from .models import BorrowingTransaction,Reservation


class BorrowingTransactionSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    borrower_name = serializers.CharField(source='borrower.user.username', read_only=True)


    class Meta:
        model = BorrowingTransaction
        fields = ['id', 'borrower', 'borrower_name', 'book', 'book_title', 'borrow_date', 'due_date', 'return_date', 'is_overdue']
        read_only_fields = ['borrow_date', 'is_overdue']

class ReservationSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    reserver_name = serializers.CharField(source='reserver.user.username', read_only=True)


    class Meta:
        model = Reservation
        fields = ['id', 'reserver', 'reserver_name', 'book', 'book_title', 'reservation_date', 'is_active']
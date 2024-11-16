from django.db import models
from borrowers.models import Borrower
from books.models import Book

class BorrowingTransaction(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE,related_name="transactions")
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name="transactions")
    borrow_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True,blank=True)

    def is_overdue(self):
        from django.utils import timezone
        return self.return_date is None and self.due_date <timezone.now().date()
    

    def __str__(self):
        return f"{self.borrower.user.username} - {self.book.title}"
class Reservation(models.Model):
    reserver = models.ForeignKey(Borrower, on_delete=models.CASCADE, related_name='reservations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='reservations')
    reservation_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def return_book(self, request, *args, **kwargs):
        transaction = self.get_object()
        transaction.return_date = timezone.now()
        transaction.save()

        # غیرفعال کردن رزرو‌های مرتبط با کتاب
        Reservation.objects.filter(book=transaction.book).update(is_active=False)

        return Response({"message": "Book returned successfully."}, status=status.HTTP_200_OK)

    def __str__(self):
        return f"Reservation by {self.reserver.user.username} for {self.book.title}"
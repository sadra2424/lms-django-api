from celery import shared_task
from django.utils import timezone
from transactions.models import BorrowingTransaction,Reservation
from django.core.mail import send_mail

@shared_task
def send_due_date_reminder():
    # کتاب‌های نزدیک به وقت پس دادنشون هست را پیدا میکند و اعلان ارسال می‌کنیم
    due_books = BorrowingTransaction.objects.filter(due_date__lte=timezone.now() + timezone.timedelta(days=2), return_date__isnull=True)

    for transaction in due_books:
        send_mail( 'Reminder: Book Due Soon',
            f'Your borrowed book "{transaction.book.title}" is due soon!',
            'from@example.com',
            [transaction.borrower.user.email],)

@shared_task
def send_reservation_available_notification():
    # کتاب‌های رزرو شده‌ای که موجود شده‌اند را پیدا می‌کنیم و اعلان ارسال می‌کنیم
    available_books = Reservation.objects.filter(is_active=True, book__availability=True)
    for reservation in available_books:
        send_mail(
            'Your Reserved Book is Available',
            f'The book "{reservation.book.title}" you reserved is now available!',
            'from@example.com',
            [reservation.borrower.user.email],
        )
        reservation.is_active = False
        reservation.save()
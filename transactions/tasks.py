from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime
from .models import BorrowingTransaction

@shared_task
def send_due_date_reminder():
    # واکشی لیست Borrowerها با تاریخ بازگشت نزدیک
    today = datetime.today().date()
    due_transactions = BorrowingTransaction.objects.filter(due_date__lte=today, return_date__isnull=True)

    for transaction in due_transactions:
        # ارسال ایمیل یادآوری برای هر Borrower
        send_mail(
            'Reminder: Book Due Date',
            f'Dear {transaction.borrower.user.username}, your borrowed book "{transaction.book.title}" is due soon. Please return it on time.',
            'from@example.com',
            [transaction.borrower.user.email],
            fail_silently=False,
        )

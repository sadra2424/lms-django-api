from celery import shared_task
from .models import Report
from books.models import Book
from borrowers.models import Borrower
import json

@shared_task
def generate_most_borrowed_books_report():
    most_borrowed_books = Book.objects.order_by('-borrow_count')[:10]
    data = [{'title': book.title, 'borrow_count': book.borrow_count} for book in most_borrowed_books]

    Report.objects.create(report_type='MOST_BORROWED', data=json.dumps(data))

@shared_task
def generate_overdue_borrowers_report():
    overdue_borrowers = Borrower.objects.filter(books__due_date__lt= timezone.now(), books__returned=False).distinct()
    data = [{'username': borrower.user.username, 'overdue_books': borrower.books.count()} for borrower in overdue_borrowers]

    Report.objects.create(report_type='OVERDUE_BORROWERS', data=json.dumps(data))


@shared_task
def generate_checked_out_books_report():
    checked_out_books = Book.objects.filter(checked_out=True)
    data = [{'title': book.title, 'borrower': book.borrower.user.username} for book in checked_out_books]

    Report.objects.create(report_type='CHECKED_OUT_BOOKS', data=json.dumps(data))
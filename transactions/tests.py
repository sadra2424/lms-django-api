import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from books.models import Book, Category
from borrowers.models import Borrower
from transactions.models import BorrowingTransaction
from django.contrib.auth import get_user_model
from authors.models import Author

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_create_borrowing_transaction(api_client):
    try:
        print("Creating author...")
        author = Author.objects.create(
            name="Sample Author",
            biography="This is a sample biography.",
            nationality="American",
            date_of_birth="1970-01-01"
        )
        print("Author created:", author)

        print("Creating borrower...")
        borrower = Borrower.objects.create(user=User.objects.create_user(username="testuser", password="testpassword"))
        print("Borrower created:", borrower)

        print("Creating category...")
        category = Category.objects.create(name="Fiction")
        print("Category created:", category)

        print("Creating book...")
        book = Book.objects.create(
            title="Sample Book",
            ISBN="1234567890123",
            category=category,
            author=author,
            publication_date="2024-01-01",
            language="English",
            availability=True
        )
        print("Book created:", book)

        print("Sending POST request to create borrowing transaction...")
        response = api_client.post(reverse('borrowingtransaction-list'), {
            "borrower": borrower.id,
            "book": book.id,
            "borrow_date": "2024-01-01",
            "due_date": "2024-01-10"
        })
        print("Response status code:", response.status_code)
        print("Response data:", response.data)

        assert response.status_code == 201
    except Exception as e:
        print("Error occurred:", e)
        raise

@pytest.mark.django_db
def test_list_borrowing_transactions(api_client):
    try:
        print("Sending GET request to list borrowing transactions...")
        response = api_client.get(reverse('borrowingtransaction-list'))
        print("Response status code:", response.status_code)
        print("Response data:", response.data)

        assert response.status_code == 200
    except Exception as e:
        print("Error occurred:", e)
        raise

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from authors.models import Author
from books.models import Book, Category

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client):
    user_data = {"username": "testuser", "password": "password123", "is_staff": True, "is_superuser": True}
    
    # ایجاد کاربر با مجوزهای لازم
    from django.contrib.auth import get_user_model
    User = get_user_model()
    User.objects.create_user(**user_data)
    
    # دریافت توکن JWT
    response = api_client.post(reverse('token_obtain_pair'), user_data)
    assert response.status_code == 200, f"Authentication failed: {response.data}"
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

@pytest.fixture(autouse=True)
def clean_db(db):
    Book.objects.all().delete()
    Category.objects.all().delete()
    Author.objects.all().delete()

@pytest.mark.django_db
def test_create_book(authenticated_client):
    # ایجاد نویسنده
    author = Author.objects.create(
        name="John Doe",
        biography="An author biography",
        nationality="American",
        date_of_birth="1980-01-01"
    )
    
    # ایجاد دسته‌بندی
    category = Category.objects.create(name="Fiction")

    # ارسال درخواست POST برای ایجاد کتاب
    response = authenticated_client.post(reverse('book-list'), {
        "title": "Sample Book",
        "description": "A great book",
        "author": author.id,
        "ISBN": "1234567890123",
        "category": category.id,
        "publication_date": "2024-01-01"
    })
    assert response.status_code == status.HTTP_201_CREATED, f"Unexpected response: {response.data}"

@pytest.mark.django_db
def test_list_books(authenticated_client):
    # ایجاد نویسنده
    author = Author.objects.create(
        name="John Doe",
        biography="An author biography",
        nationality="American",
        date_of_birth="1980-01-01"
    )

    # ایجاد دسته‌بندی
    category = Category.objects.create(name="Fiction")

    # ایجاد کتاب
    Book.objects.create(
        title="Sample Book",
        description="A great book",
        author=author,
        ISBN="1234567890123",
        category=category,
        publication_date="2024-01-01"
    )

    # ارسال درخواست GET برای لیست کتاب‌ها
    response = authenticated_client.get(reverse('book-list'))
    assert response.status_code == status.HTTP_200_OK, f"Unexpected response: {response.data}"
    assert len(response.data['results']) > 0, f"Expected at least one book. Data: {response.data}"


@pytest.mark.django_db
def test_filter_books_by_category(authenticated_client):

    # پاک‌سازی کتاب‌ها و دسته‌بندی‌ها
    Book.objects.all().delete()
    Category.objects.all().delete()
    Author.objects.all().delete()

    # ایجاد نویسنده
    author = Author.objects.create(
        name="Jane Doe",
        biography="Another author",
        nationality="Canadian",
        date_of_birth="1970-01-01"
    )

    # ایجاد دسته‌بندی
    category = Category.objects.create(name="Non-Fiction")

    # ایجاد کتاب
    Book.objects.create(
        title="Filtered Book",
        description="Book Description",
        author=author,
        ISBN="1234567890124",
        category=category,
        publication_date="2024-01-01"
    )

    # ارسال درخواست GET برای فیلتر بر اساس دسته‌بندی
    response = authenticated_client.get(reverse('book-list') + f'?category={category.id}')
    print(f"Response Data: {response.data}")

    # بهبود بررسی طول لیست نتایج
    assert response.status_code == status.HTTP_200_OK, f"Unexpected response: {response.data}"
    assert len(response.data['results']) == 1, f"Unexpected number of books: {len(response.data['results'])}. Data: {response.data['results']}"
    assert response.data['results'][0]['title'] == "Filtered Book", f"Book title mismatch: {response.data['results'][0]['title']}"

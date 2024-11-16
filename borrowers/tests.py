import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from borrowers.models import Borrower, CustomUser
from rest_framework import status
from django.contrib.auth import get_user_model

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client):
    user_data = {"username": "admin", "password": "adminpassword", "is_staff": True}
    CustomUser.objects.create_user(**user_data)

    # دریافت توکن
    response = api_client.post(reverse('token_obtain_pair'), user_data)
    assert response.status_code == status.HTTP_200_OK, "Failed to obtain token."
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.mark.django_db
def test_create_borrower(authenticated_client):
    # ارسال درخواست POST برای ایجاد Borrower
    response = authenticated_client.post(reverse('borrower-list'), {
        "username": "testuser",             # ارسال نام کاربری
        "email": "testuser@example.com",   # ارسال ایمیل
        "password": "testpassword",        # ارسال رمز عبور
        "registration_date": "2024-01-01"  # تاریخ ثبت
    })

    # بررسی وضعیت پاسخ
    assert response.status_code == status.HTTP_201_CREATED, f"Unexpected response: {response.data}"


@pytest.mark.django_db
def test_list_borrowers(authenticated_client):
    # ارسال درخواست GET برای دریافت لیست Borrower‌ها
    response = authenticated_client.get(reverse('borrower-list'))
    assert response.status_code == status.HTTP_200_OK, f"Unexpected response: {response.data}"

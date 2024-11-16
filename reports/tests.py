import pytest
from django.urls import reverse
from reports.models import Report
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user_data = {"username": "testadmin", "password": "adminpassword", "is_staff": True}
    User.objects.create_user(**user_data)
    
    # دریافت توکن
    response = api_client.post(reverse('token_obtain_pair'), user_data)
    assert response.status_code == 200, "Authentication failed."
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.mark.django_db
def test_reports_list(authenticated_client):
    response = authenticated_client.get(reverse('reports-list'))
    assert response.status_code == status.HTTP_200_OK


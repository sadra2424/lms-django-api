import pytest
from django.urls import reverse
from authors.models import Author
from rest_framework import status

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def authenticated_client(api_client):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    # Create a user with admin privileges
    user_data = {"username": "testadmin", "password": "adminpassword", "is_staff": True}
    User.objects.create_user(**user_data)
    
    # Authenticate and get the token
    response = api_client.post(reverse('token_obtain_pair'), user_data)
    assert response.status_code == 200, f"Unexpected response during authentication: {response.data}"
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

# --- Tests for Authors ---
@pytest.mark.django_db
def test_create_author(authenticated_client):
    # Make a POST request to create an author
    response = authenticated_client.post(reverse('author-list'), {
        "name": "John Doe",
        "biography": "An author biography",
        "nationality": "American",
        "date_of_birth": "1980-01-01"
    })

    # Assert response status code
    assert response.status_code == status.HTTP_201_CREATED, f"Unexpected response: {response.data}"
    assert response.data['name'] == "John Doe"

@pytest.mark.django_db
def test_list_authors(authenticated_client):
    # Make a GET request to list authors
    response = authenticated_client.get(reverse('author-list'))

    # Assert response status code
    assert response.status_code == status.HTTP_200_OK, f"Unexpected response: {response.data}"

@pytest.mark.django_db
def test_filter_authors_by_name(authenticated_client):
    # Create two authors
    Author.objects.create(name="John Doe", biography="An author biography", nationality="American", date_of_birth="1980-01-01")
    Author.objects.create(name="Jane Smith", biography="Another biography", nationality="British", date_of_birth="1985-01-01")
    
    # Filter by name
    response = authenticated_client.get(reverse('author-list') + "?search=John")
    
    # Assert only the filtered authors are returned
    assert response.status_code == status.HTTP_200_OK, f"Unexpected response: {response.data}"
    assert len(response.data['results']) == 1, f"Unexpected number of authors: {len(response.data['results'])}. Data: {response.data}"
    assert response.data['results'][0]['name'] == "John Doe"

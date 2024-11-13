import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

@pytest.mark.django_db
class TestUserAPI:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

    def test_create_user(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(reverse('user-list'), data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == 'newuser'
        assert User.objects.filter(username='newuser').exists()

    def test_create_user_missing_password(self):
        data = {
            'username': 'nouserpassword',
            'email': 'nopass@example.com',
            'first_name': 'No',
            'last_name': 'Password'
        }
        response = self.client.post(reverse('user-list'), data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST  # Assert request failed

    def test_create_user_non_allowed_username(self):
        data = {
            'username': 'Non-allowed empty space here',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(reverse('user-list'), data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST  # Assert request failed

    def test_create_user_duplicate_username(self):
        User.objects.create_user(username='existinguser', password='password')

        data = {
            'username': 'existinguser',
            'password': 'newpassword123',
            'email': 'duplicate@example.com',
            'first_name': 'Duplicate',
            'last_name': 'User'
        }
        response = self.client.post(reverse('user-list'), data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'username' in response.data
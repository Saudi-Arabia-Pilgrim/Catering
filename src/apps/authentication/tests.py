from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.models import CustomUser


class AuthenticationTests(TestCase):
    """
    Test cases for authentication functionality.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()

        # Create test users with different roles
        self.admin_user = CustomUser.objects.create_user(
            username='admin_user',
            full_name='Admin User',
            email='admin@example.com',
            role=CustomUser.UserRole.ADMIN,
            password='testpassword123'
        )

        self.hotel_user = CustomUser.objects.create_user(
            username='hotel_user',
            full_name='Hotel User',
            email='hotel@example.com',
            role=CustomUser.UserRole.HOTEL,
            password='testpassword123'
        )

        self.catering_user = CustomUser.objects.create_user(
            username='catering_user',
            full_name='Catering User',
            email='catering@example.com',
            role=CustomUser.UserRole.CATERING,
            password='testpassword123'
        )


    def test_user_login(self):
        """
        Test user login.
        """
        url = reverse('authentication:login')
        data = {
            'username': 'admin_user',
            'password': 'testpassword123'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['username'], 'admin_user')
        self.assertEqual(response.data['role'], CustomUser.UserRole.ADMIN)

    def test_token_obtain(self):
        """
        Test obtaining a JWT token.
        """
        url = reverse('authentication:token_obtain_pair')
        data = {
            'username': 'hotel_user',
            'password': 'testpassword123'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['username'], 'hotel_user')
        self.assertEqual(response.data['role'], CustomUser.UserRole.HOTEL)

    def test_token_refresh(self):
        """
        Test refreshing a JWT token.
        """
        # First, obtain a token
        url = reverse('authentication:token_obtain_pair')
        data = {
            'username': 'catering_user',
            'password': 'testpassword123'
        }

        response = self.client.post(url, data, format='json')
        refresh_token = response.data['refresh']

        # Then, refresh the token
        url = reverse('authentication:token_refresh')
        data = {
            'refresh': refresh_token
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_token_verify(self):
        """
        Test verifying a JWT token.
        """
        # First, obtain a token
        url = reverse('authentication:token_obtain_pair')
        data = {
            'username': 'admin_user',
            'password': 'testpassword123'
        }

        response = self.client.post(url, data, format='json')
        access_token = response.data['access']

        # Then, verify the token
        url = reverse('authentication:token_verify')
        data = {
            'token': access_token
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        """
        Test user logout.
        """
        # First, obtain a token
        url = reverse('authentication:token_obtain_pair')
        data = {
            'username': 'admin_user',
            'password': 'testpassword123'
        }

        response = self.client.post(url, data, format='json')
        refresh_token = response.data['refresh']
        access_token = response.data['access']

        # Set the authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Then, logout
        url = reverse('authentication:logout')
        data = {
            'refresh': refresh_token
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

        # Verify that the token is blacklisted
        url = reverse('authentication:token_refresh')
        data = {
            'refresh': refresh_token
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

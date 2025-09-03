from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class RoleBasedPermissionTests(TestCase):
    """
    Test role-based permissions functionality.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        # Create a superuser
        self.superuser = User.objects.create_superuser(
            username='superuser',
            full_name='Super User',
            email='superuser@example.com',
            password='password123'
        )
        
        # Create an admin user
        self.admin_user = User.objects.create_user(
            username='admin_user',
            full_name='Admin User',
            email='admin@example.com',
            password='password123',
            role='admin',
            is_staff=True
        )
        
        # Create a hotel user
        self.hotel_user = User.objects.create_user(
            username='hotel_user',
            full_name='Hotel User',
            email='hotel@example.com',
            password='password123',
            role='hotel'
        )
        
        # Create a catering user
        self.catering_user = User.objects.create_user(
            username='catering_user',
            full_name='Catering User',
            email='catering@example.com',
            password='password123',
            role='catering'
        )
        
        # Set up API client
        self.client = APIClient()
    
    def test_superuser_can_access_all_users(self):
        """
        Test that a superuser can access all users.
        """
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # All 4 users
    
    def test_admin_can_access_all_users(self):
        """
        Test that an admin user can access all users.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # All 4 users
    
    def test_hotel_user_can_only_access_self(self):
        """
        Test that a hotel user can only access their own user data.
        """
        self.client.force_authenticate(user=self.hotel_user)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only themselves
        self.assertEqual(response.data[0]['username'], 'hotel_user')
    
    def test_catering_user_can_only_access_self(self):
        """
        Test that a catering user can only access their own user data.
        """
        self.client.force_authenticate(user=self.catering_user)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only themselves
        self.assertEqual(response.data[0]['username'], 'catering_user')
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.users.models import CustomUser
from apps.base.mixins import (
    AdminAccessMixin,
    HotelAccessMixin,
    CateringAccessMixin
)


# Example views for testing role-based access
class AdminOnlyView(AdminAccessMixin, APIView):
    def get(self, request):
        return Response({"message": "Admin only content"})


class HotelOnlyView(HotelAccessMixin, APIView):
    def get(self, request):
        return Response({"message": "Hotel only content"})


class CateringOnlyView(CateringAccessMixin, APIView):
    def get(self, request):
        return Response({"message": "Catering only content"})


class RoleBasedPermissionTests(APITestCase):
    """
    Test cases for role-based permissions.
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
        
        # Register the test views
        from django.urls import path
        from django.conf.urls import include
        
        urlpatterns = [
            path('admin-only/', AdminOnlyView.as_view(), name='admin-only'),
            path('hotel-only/', HotelOnlyView.as_view(), name='hotel-only'),
            path('catering-only/', CateringOnlyView.as_view(), name='catering-only'),
        ]
        
        from django.conf import settings
        settings.ROOT_URLCONF = __name__
    
    def test_admin_access(self):
        """
        Test that admin users can access admin-only views.
        """
        # Get JWT token for admin user
        response = self.client.post('/api/v1/auth/token/', {
            'username': 'admin_user',
            'password': 'testpassword123'
        }, format='json')
        
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Admin should be able to access admin-only view
        response = self.client.get('/admin-only/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Admin should not be able to access hotel-only view
        response = self.client.get('/hotel-only/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Admin should not be able to access catering-only view
        response = self.client.get('/catering-only/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_hotel_access(self):
        """
        Test that hotel users can access hotel-only views.
        """
        # Get JWT token for hotel user
        response = self.client.post('/api/v1/auth/token/', {
            'username': 'hotel_user',
            'password': 'testpassword123'
        }, format='json')
        
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Hotel user should not be able to access admin-only view
        response = self.client.get('/admin-only/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Hotel user should be able to access hotel-only view
        response = self.client.get('/hotel-only/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Hotel user should not be able to access catering-only view
        response = self.client.get('/catering-only/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_catering_access(self):
        """
        Test that catering users can access catering-only views.
        """
        # Get JWT token for catering user
        response = self.client.post('/api/v1/auth/token/', {
            'username': 'catering_user',
            'password': 'testpassword123'
        }, format='json')
        
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Catering user should not be able to access admin-only view
        response = self.client.get('/admin-only/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Catering user should not be able to access hotel-only view
        response = self.client.get('/hotel-only/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Catering user should be able to access catering-only view
        response = self.client.get('/catering-only/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_access(self):
        """
        Test that unauthenticated users cannot access any protected views.
        """
        # Clear any existing credentials
        self.client.credentials()
        
        # Unauthenticated user should not be able to access admin-only view
        response = self.client.get('/admin-only/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Unauthenticated user should not be able to access hotel-only view
        response = self.client.get('/hotel-only/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Unauthenticated user should not be able to access catering-only view
        response = self.client.get('/catering-only/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
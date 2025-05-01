"""
Tests for the users app views.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserViewSetTests(APITestCase):
    """
    Tests for the UserViewSet.
    """
    
    def setUp(self):
        """
        Set up test data.
        """
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
        }
        self.user = User.objects.create_user(**self.user_data)
        
        # Get tokens for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # URLs
        self.user_list_url = reverse("user-list")
        self.user_detail_url = reverse("user-detail", kwargs={"pk": self.user.pk})
        self.user_me_url = reverse("user-me")
    
    def test_list_users_authenticated(self):
        """
        Test listing users when authenticated.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
    
    def test_list_users_unauthenticated(self):
        """
        Test listing users when unauthenticated.
        """
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_retrieve_user_authenticated(self):
        """
        Test retrieving a user when authenticated.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])
    
    def test_retrieve_user_unauthenticated(self):
        """
        Test retrieving a user when unauthenticated.
        """
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_user(self):
        """
        Test creating a user.
        """
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "password_confirm": "newpassword",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(self.user_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(email=data["email"]).first_name, data["first_name"])
    
    def test_update_user_authenticated(self):
        """
        Test updating a user when authenticated.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        data = {
            "first_name": "Updated",
            "last_name": "Name",
        }
        response = self.client.patch(self.user_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, data["first_name"])
        self.assertEqual(self.user.last_name, data["last_name"])
    
    def test_update_user_unauthenticated(self):
        """
        Test updating a user when unauthenticated.
        """
        data = {
            "first_name": "Updated",
            "last_name": "Name",
        }
        response = self.client.patch(self.user_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_me_endpoint_authenticated(self):
        """
        Test the me endpoint when authenticated.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        response = self.client.get(self.user_me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user_data["email"])
    
    def test_me_endpoint_unauthenticated(self):
        """
        Test the me endpoint when unauthenticated.
        """
        response = self.client.get(self.user_me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

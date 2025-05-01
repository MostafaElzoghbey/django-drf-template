"""
Tests for the authentication app views.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class AuthenticationViewsTests(APITestCase):
    """
    Tests for the authentication views.
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
        self.refresh_token = str(refresh)
        self.access_token = str(refresh.access_token)
        
        # URLs
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.token_url = reverse("token_obtain_pair")
        self.token_refresh_url = reverse("token_refresh")
        self.token_verify_url = reverse("token_verify")
    
    def test_login(self):
        """
        Test logging in.
        """
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data["data"])
        self.assertIn("access", response.data["data"])
        self.assertIn("user", response.data["data"])
        self.assertEqual(response.data["data"]["user"]["email"], self.user_data["email"])
    
    def test_login_invalid_credentials(self):
        """
        Test logging in with invalid credentials.
        """
        data = {
            "email": self.user_data["email"],
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_logout(self):
        """
        Test logging out.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        data = {
            "refresh": self.refresh_token,
        }
        response = self.client.post(self.logout_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_token_obtain_pair(self):
        """
        Test obtaining a token pair.
        """
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)
        self.assertIn("user", response.data)
    
    def test_token_refresh(self):
        """
        Test refreshing a token.
        """
        data = {
            "refresh": self.refresh_token,
        }
        response = self.client.post(self.token_refresh_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data["data"])
    
    def test_token_verify(self):
        """
        Test verifying a token.
        """
        data = {
            "token": self.access_token,
        }
        response = self.client.post(self.token_verify_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

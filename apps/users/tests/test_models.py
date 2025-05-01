"""
Tests for the users app models.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTests(TestCase):
    """
    Tests for the User model.
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
    
    def test_create_user(self):
        """
        Test creating a user.
        """
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertEqual(self.user.first_name, self.user_data["first_name"])
        self.assertEqual(self.user.last_name, self.user_data["last_name"])
        self.assertTrue(self.user.check_password(self.user_data["password"]))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.user.is_active)
    
    def test_create_superuser(self):
        """
        Test creating a superuser.
        """
        superuser = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword",
        )
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertTrue(superuser.check_password("adminpassword"))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
    
    def test_get_full_name(self):
        """
        Test getting the full name.
        """
        self.assertEqual(
            self.user.get_full_name(), f"{self.user_data['first_name']} {self.user_data['last_name']}"
        )
    
    def test_get_short_name(self):
        """
        Test getting the short name.
        """
        self.assertEqual(self.user.get_short_name(), self.user_data["first_name"])

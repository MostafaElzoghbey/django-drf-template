"""
Token service for the authentication app.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def get_tokens_for_user(user):
    """
    Get JWT tokens for a user.
    
    Args:
        user: The user to get tokens for.
        
    Returns:
        A dictionary containing the refresh and access tokens.
    """
    refresh = RefreshToken.for_user(user)
    
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def generate_password_reset_token(user):
    """
    Generate a password reset token for a user.
    
    Args:
        user: The user to generate a token for.
        
    Returns:
        A tuple containing the UID and token.
    """
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    return uid, token


def generate_email_verification_token(user):
    """
    Generate an email verification token for a user.
    
    Args:
        user: The user to generate a token for.
        
    Returns:
        A tuple containing the UID and token.
    """
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    return uid, token

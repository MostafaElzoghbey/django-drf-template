"""
URL configuration for the authentication app.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from apps.authentication.views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    EmailVerificationView,
    LoginView,
    LogoutView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
)

urlpatterns = [
    # JWT token endpoints
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    
    # Login and logout
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    
    # Password reset
    path(
        "password/reset/",
        PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    
    # Email verification
    path(
        "email/verify/",
        EmailVerificationView.as_view(),
        name="email_verification",
    ),
]

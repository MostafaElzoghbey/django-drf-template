"""
Views for the authentication app.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.authentication.serializers import (
    CustomTokenObtainPairSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
)
from apps.core.utils.helpers import format_response
from apps.core.schemas import custom_extend_schema

User = get_user_model()


@custom_extend_schema(
    summary="Obtain JWT token",
    description="Obtain JWT token pair (access and refresh tokens)",
    tags=["Authentication"],
)
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain pair view that uses our custom serializer.
    """

    serializer_class = CustomTokenObtainPairSerializer


@custom_extend_schema(
    summary="Refresh JWT token",
    description="Refresh JWT access token using refresh token",
    tags=["Authentication"],
)
class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom token refresh view.
    """

    @custom_extend_schema(
        summary="Refresh token",
        description="Get a new access token using a refresh token",
        tags=["Authentication"],
    )
    def post(self, request, *args, **kwargs):
        """
        Return a refreshed token.
        """
        response = super().post(request, *args, **kwargs)

        # Format the response
        return Response(
            format_response(
                data=response.data,
                message="Token refreshed successfully",
            ),
            status=response.status_code,
        )


class LoginView(APIView):
    """
    View for user login.
    """

    permission_classes = [AllowAny]

    @custom_extend_schema(
        request=LoginSerializer,
        summary="User login",
        description="Log in a user and return a token",
        tags=["Authentication"],
    )
    def post(self, request):
        """
        Log in a user and return a token.
        """
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]

        return Response(
            format_response(
                data={
                    "refresh": refresh,
                    "access": access,
                    "user": {
                        "id": str(user.id),
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                },
                message="Login successful",
            )
        )


class LogoutView(APIView):
    """
    View for user logout.
    """

    permission_classes = [IsAuthenticated]

    @custom_extend_schema(
        request={
            "type": "object",
            "properties": {
                "refresh": {
                    "type": "string",
                    "description": "Refresh token to blacklist",
                }
            },
            "required": ["refresh"],
        },
        summary="User logout",
        description="Log out a user by blacklisting their refresh token",
        tags=["Authentication"],
    )
    def post(self, request):
        """
        Log out a user by blacklisting their refresh token.
        """
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            return Response(
                format_response(message="Logout successful"),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                format_response(
                    status="error",
                    code=status.HTTP_400_BAD_REQUEST,
                    message=str(e),
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordResetRequestView(APIView):
    """
    View for requesting a password reset.
    """

    permission_classes = [AllowAny]

    @custom_extend_schema(
        request=PasswordResetRequestSerializer,
        summary="Request password reset",
        description="Request a password reset email",
        tags=["Authentication"],
    )
    def post(self, request):
        """
        Request a password reset.
        """
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)

            # Generate token and UID
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # In a real application, you would send an email with the reset link
            # For this template, we'll just return the token and UID
            reset_link = f"/reset-password/{uid}/{token}/"

            # TODO: Send email with reset link

            return Response(
                format_response(
                    message="Password reset email sent",
                    data={"reset_link": reset_link},  # Remove this in production
                ),
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            # We don't want to reveal that the email doesn't exist
            return Response(
                format_response(message="Password reset email sent"),
                status=status.HTTP_200_OK,
            )


class PasswordResetConfirmView(APIView):
    """
    View for confirming a password reset.
    """

    permission_classes = [AllowAny]

    @custom_extend_schema(
        request=PasswordResetConfirmSerializer,
        summary="Confirm password reset",
        description="Confirm a password reset with token and set new password",
        tags=["Authentication"],
    )
    def post(self, request):
        """
        Confirm a password reset.
        """
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            # Decode the UID
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)

            # Check if the token is valid
            if not default_token_generator.check_token(user, token):
                return Response(
                    format_response(
                        status="error",
                        code=status.HTTP_400_BAD_REQUEST,
                        message="Invalid token",
                    ),
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Set the new password
            user.set_password(new_password)
            user.save()

            return Response(
                format_response(message="Password reset successful"),
                status=status.HTTP_200_OK,
            )
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                format_response(
                    status="error",
                    code=status.HTTP_400_BAD_REQUEST,
                    message="Invalid UID",
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )


class EmailVerificationView(APIView):
    """
    View for email verification.
    """

    permission_classes = [AllowAny]

    @custom_extend_schema(
        request=EmailVerificationSerializer,
        summary="Verify email",
        description="Verify a user's email address with token",
        tags=["Authentication"],
    )
    def post(self, request):
        """
        Verify a user's email.
        """
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]

        try:
            # Decode the UID
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)

            # Check if the token is valid
            if not default_token_generator.check_token(user, token):
                error_code = status.HTTP_400_BAD_REQUEST
                return Response(
                    format_response(
                        status="error",
                        code=error_code,
                        message="Invalid token",
                    ),
                    status=error_code,
                )

            # Mark the email as verified
            user.email_verified = True
            user.save()

            success_code = status.HTTP_200_OK
            return Response(
                format_response(
                    status="success",
                    code=success_code,
                    message="Email verified successfully",
                ),
                status=success_code,
            )
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            error_code = status.HTTP_400_BAD_REQUEST
            return Response(
                format_response(
                    status="error",
                    code=error_code,
                    message="Invalid UID",
                ),
                status=error_code,
            )

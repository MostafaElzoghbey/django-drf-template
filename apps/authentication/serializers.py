"""
Serializers for the authentication app.
"""

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer that includes user data in the response.
    """
    
    def validate(self, attrs):
        """
        Validate the user credentials and return the token.
        """
        data = super().validate(attrs)
        
        # Add user data to the response
        user = self.user
        data.update(
            {
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            }
        )
        
        return data


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        """
        Validate the user credentials and return the token.
        """
        email = attrs.get("email")
        password = attrs.get("password")
        
        if email and password:
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )
            
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            
            if not user.is_active:
                msg = _("User account is disabled.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _("Must include 'email' and 'password'.")
            raise serializers.ValidationError(msg, code="authorization")
        
        # Generate token
        refresh = RefreshToken.for_user(user)
        
        attrs["user"] = user
        attrs["refresh"] = str(refresh)
        attrs["access"] = str(refresh.access_token)
        
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.
    """
    
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        """
        Validate that the email exists.
        """
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            # We don't want to reveal that the email doesn't exist
            pass
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset.
    """
    
    token = serializers.CharField(required=True)
    uid = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        """
        Validate that the passwords match.
        """
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password_confirm": "Password fields didn't match."}
            )
        return attrs


class EmailVerificationSerializer(serializers.Serializer):
    """
    Serializer for email verification.
    """
    
    token = serializers.CharField(required=True)
    uid = serializers.CharField(required=True)

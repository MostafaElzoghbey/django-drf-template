"""
Serializers for the users app.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.core.serializers import BaseModelSerializer

User = get_user_model()


class UserSerializer(BaseModelSerializer):
    """
    Serializer for the User model.
    """
    
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "bio",
            "profile_picture",
            "phone_number",
            "date_joined",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "date_joined", "created_at", "updated_at"]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    """
    
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
        ]
    
    def validate(self, attrs):
        """
        Validate that the passwords match.
        """
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Password fields didn't match."}
            )
        return attrs
    
    def create(self, validated_data):
        """
        Create and return a new user.
        """
        # Remove password_confirm from validated_data
        validated_data.pop("password_confirm")
        
        # Create the user
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a user.
    """
    
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "bio",
            "profile_picture",
            "phone_number",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.
    """
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """
        Validate that the new passwords match.
        """
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password_confirm": "Password fields didn't match."}
            )
        return attrs
    
    def validate_old_password(self, value):
        """
        Validate that the old password is correct.
        """
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

"""
Base serializers for the project.
"""

from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base serializer for model serializers.
    
    This serializer provides common functionality for all model serializers.
    """
    
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        fields = ["id", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class BaseSerializer(serializers.Serializer):
    """
    Base serializer for non-model serializers.
    
    This serializer provides common functionality for all non-model serializers.
    """
    
    def create(self, validated_data):
        """
        Create method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement create()")
    
    def update(self, instance, validated_data):
        """
        Update method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement update()")

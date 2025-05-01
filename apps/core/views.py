"""
Base views for the project.
"""

from rest_framework import mixins, viewsets
from rest_framework.response import Response

from apps.core.utils.helpers import format_response


class BaseViewSet(viewsets.GenericViewSet):
    """
    Base viewset for all viewsets.
    
    This viewset provides common functionality for all viewsets.
    """
    
    def get_success_headers(self, data):
        """
        Get success headers for create operations.
        """
        try:
            return {"Location": str(data["id"])}
        except (TypeError, KeyError):
            return {}
    
    def get_response(self, data=None, status="success", code=200, message=None, errors=None):
        """
        Get a formatted response.
        """
        return Response(
            format_response(
                data=data, status=status, code=code, message=message, errors=errors
            ),
            status=code,
        )


class ReadOnlyViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, BaseViewSet
):
    """
    A viewset that provides default `retrieve()` and `list()` actions.
    """
    pass


class ModelViewSet(viewsets.ModelViewSet, BaseViewSet):
    """
    A viewset that provides default CRUD actions.
    """
    
    def create(self, request, *args, **kwargs):
        """
        Create a model instance.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            format_response(
                data=serializer.data,
                message="Resource created successfully",
            ),
            status=201,
            headers=headers,
        )
    
    def update(self, request, *args, **kwargs):
        """
        Update a model instance.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        
        return Response(
            format_response(
                data=serializer.data,
                message="Resource updated successfully",
            )
        )
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a model instance.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            format_response(
                message="Resource deleted successfully",
            ),
            status=204,
        )

"""
Custom filter backends for the project.
"""

from django_filters import rest_framework as filters
from rest_framework.filters import BaseFilterBackend


class BaseFilterSet(filters.FilterSet):
    """
    Base filter set for all filter sets.
    
    This filter set provides common functionality for all filter sets.
    """
    
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    updated_after = filters.DateTimeFilter(field_name="updated_at", lookup_expr="gte")
    updated_before = filters.DateTimeFilter(field_name="updated_at", lookup_expr="lte")


class OwnerFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)

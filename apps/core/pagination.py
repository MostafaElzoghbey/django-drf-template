"""
Custom pagination classes for the project.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from apps.core.utils.helpers import format_response


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class for the project.

    This pagination class provides a consistent pagination format across the API.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Return a paginated response in a consistent format.
        """

        pagination_data = {
            "count": self.page.paginator.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
        }

        return Response(
            format_response(data=pagination_data, status="success", code=200)
        )

"""
Views for the API app.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.core.utils.helpers import format_response


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    """
    API root view that provides information about the API.
    """
    return Response(
        format_response(
            data={
                "name": "Django DRF Template API",
                "version": "1.0.0",
                "description": "A professional, reusable Django REST Framework template for building scalable and maintainable APIs.",
                "endpoints": {
                    "users": "/api/v1/users/",
                    "auth": "/api/v1/auth/",
                    "docs": "/api/docs/",
                },
            }
        )
    )

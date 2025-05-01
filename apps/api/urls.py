"""
URL configuration for the API app.
"""

from django.urls import include, path

from apps.api.views import api_root

urlpatterns = [
    # API root
    path("", api_root, name="api-root"),
    # Include other app URLs here
    path("users/", include("apps.users.urls")),
    path("auth/", include("apps.authentication.urls")),
    # Add more API endpoints as needed
]

"""
URL configuration for the users app.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.views import UserViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

# The API URLs are now determined automatically by the router
urlpatterns = [
    path("", include(router.urls)),
]

"""
Views for the users app.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.core.views import ModelViewSet
from apps.users.serializers import (
    ChangePasswordSerializer,
    UserCreateSerializer,
    UserSerializer,
    UserUpdateSerializer,
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    ViewSet for the User model.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the action.
        """
        if self.action == "create":
            return UserCreateSerializer
        elif self.action == "update" or self.action == "partial_update":
            return UserUpdateSerializer
        elif self.action == "change_password":
            return ChangePasswordSerializer
        return UserSerializer

    def get_queryset(self):
        """
        Return the queryset for the view.
        """
        # Regular users can only see their own profile
        if not self.request.user.is_staff:
            return User.objects.filter(id=self.request.user.id)
        # Staff users can see all users
        return User.objects.all()

    @action(detail=False, methods=["get"])
    def me(self, request):
        """
        Return the current user's profile.
        """
        serializer = self.get_serializer(request.user)
        return self.get_response(
            data=serializer.data, message="User profile retrieved successfully"
        )

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """
        Change the current user's password.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Change the password
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return self.get_response(
            message="Password changed successfully.", code=status.HTTP_200_OK
        )

"""
permissions.py: File, containing custom permissions for a jauth application.
"""


from __future__ import annotations
from typing import TYPE_CHECKING
from rest_framework import permissions
from rest_framework.request import Request
from jauth.models import User


if TYPE_CHECKING:
    from jauth.views import UserViewSet


class IsUserOwner(permissions.BasePermission):
    """
    IsUserOwner: Custom permission that checks whether user owns an account.

    Args:
        permissions.BasePermission (_type_): Builtin superclass for an IsUserOwner permission.
    """

    def has_object_permission(self, request: Request, view: UserViewSet, user: User) -> bool:
        """
        has_object_permission: Checks if user that sends request has permissions on user resource.

        Args:
            request (Request): Request insance.
            view (UserViewSet): Viewset instance.
            user (User): User instance.

        Returns:
            bool: Value that show if user has permission on object.
        """

        return request.user == user

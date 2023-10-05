"""
permissions.py: File, containing custom permissions for an auth application.
"""


from rest_framework import permissions
from rest_framework.request import Request

from auth.models import User
from auth.viewsets import UserViewSet


class IsUserOwner(permissions.BasePermission):
    """
    IsUserOwner: Custom permission that checks whether user owns an account.

    Args:
        permissions (_type_): Builtin superclass for an IsUserOwner permission.
    """

    def has_object_permission(self, request: Request, view: UserViewSet, user: User) -> bool:
        return request.user == user

"""
permissions.py: File, containing custom permissions for a customer application.
"""


from __future__ import annotations
from typing import TYPE_CHECKING
from rest_framework import permissions
from rest_framework.request import Request
from customer.models import CustomerModel


if TYPE_CHECKING:
    from customer.views import CustomerViewSet


class IsUserHasNotCustomer(permissions.BasePermission):
    """
    IsUserHasNotCustomer: Customer permission that checks if user has customer.

    Args:
        permissions.BasePermission (_type_): Builtin superclass for an IsUserOwner permission.
    """

    def has_permission(self, request: Request, view: CustomerViewSet) -> bool:
        """
        has_permission: Checks if user has customer.

        Args:
            request (Request): Request instance.
            view (CustomerViewSet): CustomerViewSet.

        Returns:
            bool: True if has not otherwise False.
        """

        return not hasattr(request.user, 'customermodel')


class IsCustomerOwner(permissions.BasePermission):
    """
    IsCustomerOwner: Customer permission that checks if user owns customer.

    Args:
        permissions.BasePermission (_type_): Builtin superclass for an IsUserOwner permission.
    """

    def has_object_permission(
        self, request: Request, view: CustomerViewSet, customer: CustomerModel
    ) -> bool:
        """
        has_object_permission: Checks if user owns customer.

        Args:
            request (Request): Request instance.
            view (CustomerViewSet): CustomerViewSet.
            customer (CustomerModel): Customer instance.

        Returns:
            bool: True if owns otherwise False.
        """

        return (
            not IsUserHasNotCustomer.has_permission(self, request, view)
            and request.user.customermodel == customer
        )

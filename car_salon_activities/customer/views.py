"""
views.py: File, containing views for a customer application.
"""


from typing import ClassVar
from rest_framework import status, viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.db.models.query import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from customer.models import CustomerModel, CustomerOffer
from customer.swagger import (
    customer_list_schema_extension,
    customer_create_schema_extension,
    customer_update_schema_extension,
    customer_destroy_schema_extension,
    customer_retrieve_schema_extension,
    customer_make_offer_schema_extensions,
    customer_get_statistics_schema_extension,
    customer_partial_update_schema_extension,
)
from customer.services import CustomerService
from customer.permissions import IsCustomerOwner, IsUserHasNotCustomer
from customer.serializers import (
    CustomerSerializer,
    CustomerOfferSerializer,
    CustomerHistorySerializer,
)


@extend_schema(tags=['Customer'])
@extend_schema_view(
    list=extend_schema(**customer_list_schema_extension),
    update=extend_schema(**customer_update_schema_extension),
    create=extend_schema(**customer_create_schema_extension),
    destroy=extend_schema(**customer_destroy_schema_extension),
    retrieve=extend_schema(**customer_retrieve_schema_extension),
    partial_update=extend_schema(**customer_partial_update_schema_extension),
    get_statistics=extend_schema(**customer_get_statistics_schema_extension),
    make_offer=extend_schema(**customer_make_offer_schema_extensions),
)
class CustomerViewSet(viewsets.ModelViewSet):
    """
    CustomerViewSet: Handling every action for a Customer resource.
    Maps HTTP methods to actions:
        HEAD -> list
        HEAD -> retrieve
        GET -> list
        GET -> retrieve
        POST -> create
        PUT -> update
        PATCH -> partial_update
        DELETE -> destroy

    Args:
        viewsets.ModelViewSet (_type_): Builtin superclass for a CustomerViewSet.
    """

    serializer_class: ClassVar[type[CustomerSerializer]] = CustomerSerializer

    queryset: ClassVar[QuerySet[CustomerModel]] = CustomerModel.objects.all()

    service: ClassVar[CustomerService] = CustomerService()

    permission_map: ClassVar[dict] = {
        'create': [
            IsAuthenticated & IsUserHasNotCustomer,
        ],
        'list': [
            IsAuthenticated & IsAdminUser,
        ],
        'retrieve': [
            IsAuthenticated & (IsCustomerOwner | IsAdminUser),
        ],
        'update': [
            IsAuthenticated & IsAdminUser,
        ],
        'partial_update': [
            IsAuthenticated & IsAdminUser,
        ],
        'destroy': [
            IsAuthenticated & IsAdminUser,
        ],
        'get_statistics': [
            IsAuthenticated & (IsCustomerOwner | IsAdminUser),
        ],
        'make_offer': [
            IsAuthenticated & (IsCustomerOwner | IsAdminUser),
        ],
    }

    def get_permissions(self) -> list:
        """
        get_permissions: Returns apropriate permission classes according to action.

        Returns:
            list: Permission classes.
        """

        self.permission_classes: list = self.permission_map.get(self.action, [])
        return super().get_permissions()

    def create(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        create: Creates customer object for current user.

        Args:
            request (Request): Request instance.

        Returns:
            Response: HTTP 200 if it is first try, otherwise HTTP 401/403.
        """

        if 'balance' in request.data:
            request.data.pop('balance')

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer: CustomerSerializer) -> None:
        """
        perform_create: Connect user and customer instances and also creates customer itself.

        Args:
            serializer (CustomerSerializer): CustomerSerializer instance.
        """

        serializer.save(user=self.request.user)

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        destroy: Instead of deleting from database this method set customers's is_active to False.

        Args:
            request (Request): Request instance.

        Returns:
            Response: HTTP 204 Response if customer can be deleted otherwise HTTP 401/403.
        """

        self.service.delete_customer(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, serializer_class=CustomerHistorySerializer)
    def get_statistics(self, request: Request, pk: int) -> Response:
        """
        get_statistics: Returns statistics for customer's operations.

        Args:
            request (Request): Request instance.
            pk (int): Customer's pk.

        Returns:
            Response: HTTP 200 if has permissions otherwise 401/403.
        """

        customer: CustomerModel = self.get_object()
        history: QuerySet = customer.history.all()
        serializer: CustomerHistorySerializer = self.get_serializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, serializer_class=CustomerOfferSerializer)
    def make_offer(self, request: Request, pk: int) -> Response:
        """
        make_offer: Makes customer's offer.

        Args:
            request (Request): Request instance.
            pk (int): Customer's pk.

        Returns:
            Response: Response instance.
        """

        serializer: CustomerOfferSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        offer: CustomerOffer = serializer.save(customer=self.get_object())
        self.service.make_offer(offer)
        return Response(status=status.HTTP_200_OK)

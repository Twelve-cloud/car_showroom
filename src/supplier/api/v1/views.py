"""
views.py: File, containing views for a supplier application.
"""


from typing import ClassVar
from rest_framework import status, viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.db.models.query import QuerySet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from supplier.models import SupplierModel
from supplier.services import SupplierService
from supplier.api.v1.swagger import (
    supplier_list_schema_extension,
    supplier_create_schema_extension,
    supplier_update_schema_extension,
    supplier_destroy_schema_extension,
    supplier_get_cars_schema_extension,
    supplier_retrieve_schema_extension,
    supplier_get_discounts_schema_extension,
    supplier_make_discount_schema_extension,
    supplier_get_statistics_schema_extension,
    supplier_partial_update_schema_extension,
)
from supplier.api.v1.serializers import (
    SupplierSerializer,
    SupplierCarSerializer,
    SupplierHistorySerializer,
    SupplierCarDiscountSerializer,
)


@extend_schema(tags=['Supplier'])
@extend_schema_view(
    list=extend_schema(**supplier_list_schema_extension),
    update=extend_schema(**supplier_update_schema_extension),
    create=extend_schema(**supplier_create_schema_extension),
    destroy=extend_schema(**supplier_destroy_schema_extension),
    retrieve=extend_schema(**supplier_retrieve_schema_extension),
    partial_update=extend_schema(**supplier_partial_update_schema_extension),
    make_discount=extend_schema(**supplier_make_discount_schema_extension),
    get_discounts=extend_schema(**supplier_get_discounts_schema_extension),
    get_statistics=extend_schema(**supplier_get_statistics_schema_extension),
    get_cars=extend_schema(**supplier_get_cars_schema_extension),
)
class SupplierViewSet(viewsets.ModelViewSet):
    """
    SupplierViewSet: Handling every action for a Supplier resource.
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
        viewsets.ModelViewSet (_type_): Builtin superclass for a SupplierViewSet.
    """

    queryset: ClassVar[QuerySet[SupplierModel]] = SupplierModel.objects.all()

    serializer_class: ClassVar[type[SupplierSerializer]] = SupplierSerializer

    service: ClassVar[SupplierService] = SupplierService()

    permission_classes: ClassVar[list] = [IsAdminUser]

    filter_backends: ClassVar[list] = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields: ClassVar[list] = [
        'name',
        'creation_year',
    ]

    search_fields: ClassVar[list] = [
        'name',
        'creation_year',
    ]

    ordering_fields: ClassVar[list] = [
        'name',
        'creation_year',
    ]

    ordering: ClassVar[list] = [
        '-created_at',
    ]

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        destroy: Instead of deleting from database this method set suppliers's is_active to False.

        Args:
            request (Request): Request instance.

        Returns:
            Response: HTTP 204 Response if supplier can be deleted otherwise HTTP 401/403.
        """

        self.service.delete_supplier(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True, serializer_class=SupplierCarDiscountSerializer)
    def make_discount(self, request: Request, pk: int) -> Response:
        """
        make_discount: Creates supplier car discount.

        Args:
            request (Request): Request instance.
            pk (int): Supplier's pk.

        Returns:
            Response: HTTP 200 if has permissions otherwise 401/403.
        """

        supplier: SupplierModel = self.get_object()
        serializer: SupplierCarDiscountSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(supplier=supplier)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=['get'], detail=True, serializer_class=SupplierCarDiscountSerializer)
    def get_discounts(self, request: Request, pk: int) -> Response:
        """
        get_discounts: Return discounts of the supplier.

        Args:
            request (Request): Request instance.
            pk (int): Supplier's pk.

        Returns:
            Response: HTTP 200 if has permissions otherwise 401/403.
        """

        supplier: SupplierModel = self.get_object()
        discounts: QuerySet = supplier.discounts.all()
        serializer: SupplierCarDiscountSerializer = self.get_serializer(discounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, serializer_class=SupplierHistorySerializer)
    def get_statistics(self, request: Request, pk: int) -> Response:
        """
        get_statistics: Returns statistics for suppliers's operations.

        Args:
            request (Request): Request instance.
            pk (int): Supplier's pk.

        Returns:
            Response: HTTP 200 if has permissions otherwise 401/403.
        """

        supplier: SupplierModel = self.get_object()
        history: QuerySet = supplier.history.all()
        serializer: SupplierHistorySerializer = self.get_serializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, serializer_class=SupplierCarSerializer)
    def get_cars(self, request: Request, pk: int) -> Response:
        """
        get_cars: Returns cars of the supplier.

        Args:
            request (Request): Request instance.
            pk (int): Supplier's pk.

        Returns:
            Response: HTTP 200 if has permissions otherwise 401/403.
        """

        supplier: SupplierModel = self.get_object()
        cars: QuerySet = supplier.cars.all()
        serializer: SupplierCarSerializer = self.get_serializer(cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

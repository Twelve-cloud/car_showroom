"""
views.py: File, containing views for a showroom application.
"""


from typing import ClassVar, Iterable
from rest_framework import status, viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.db.models.query import QuerySet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from showroom.models import ShowroomModel
from showroom.swagger import (
    showroom_list_schema_extension,
    showroom_create_schema_extension,
    showroom_update_schema_extension,
    showroom_destroy_schema_extension,
    showroom_get_cars_schema_extension,
    showroom_retrieve_schema_extension,
    showroom_get_discounts_schema_extension,
    showroom_make_discount_schema_extension,
    showroom_get_statistics_schema_extension,
    showroom_partial_update_schema_extension,
)
from showroom.services import ShowroomService
from showroom.serializers import (
    ShowroomSerializer,
    ShowroomCarSerializer,
    ShowroomHistorySerializer,
    ShowroomCarDiscountSerializer,
)


@extend_schema(tags=['Showroom'])
@extend_schema_view(
    list=extend_schema(**showroom_list_schema_extension),
    update=extend_schema(**showroom_update_schema_extension),
    create=extend_schema(**showroom_create_schema_extension),
    destroy=extend_schema(**showroom_destroy_schema_extension),
    retrieve=extend_schema(**showroom_retrieve_schema_extension),
    partial_update=extend_schema(**showroom_partial_update_schema_extension),
    make_discount=extend_schema(**showroom_make_discount_schema_extension),
    get_discounts=extend_schema(**showroom_get_discounts_schema_extension),
    get_statistics=extend_schema(**showroom_get_statistics_schema_extension),
    get_cars=extend_schema(**showroom_get_cars_schema_extension),
)
class ShowroomViewSet(viewsets.ModelViewSet):
    """
    ShowroomViewSet: Handling every action for a Showroom resource.
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
        viewsets.ModelViewSet (_type_): Builtin superclass for a ShowroomViewSet.
    """

    queryset: ClassVar[QuerySet[ShowroomModel]] = ShowroomModel.objects.all()

    serializer_class: ClassVar[type[ShowroomSerializer]] = ShowroomSerializer

    service: ClassVar[ShowroomService] = ShowroomService()

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

    def create(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        create: Creates showroom, finds appropriates cars and suppliers for showroom.

        Args:
            request (Request): Request instance.

        Returns:
            Response: HTTP 201 if everything is correct, otherwise HTTP 400/401/403.
        """

        serializer: ShowroomSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cars: Iterable = self.service.find_appropriate_cars(request.data)
        showroom: ShowroomModel = serializer.save()
        self.service.add_appropriate_cars(showroom, cars)
        self.service.find_appropriate_suppliers(showroom)

        headers: dict = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        update: Updates showroom and if charts is updated then finds appropriate cars and suppliers.

        Args:
            request (Request): Request instance.

        Returns:
            Response: Response instance.
        """

        if 'charts' in request.data:
            cars: Iterable = self.service.find_appropriate_cars(request.data)
            showroom: ShowroomModel = self.get_object()
            self.service.add_appropriate_cars(showroom, cars)
            self.service.find_appropriate_suppliers(showroom)

        response: Response = super().update(request, *args, **kwargs)
        return response

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        destroy: Instead of deleting from database this method set showrooms's is_active to False.

        Args:
            request (Request): Request instance.

        Returns:
            Response: HTTP 204 Response if showroom can be deleted otherwise HTTP 401/403.
        """

        self.service.delete_showroom(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True, serializer_class=ShowroomCarDiscountSerializer)
    def make_discount(self, request: Request, pk: int) -> Response:
        """
        make_discount: Creates showroom car discount.

        Args:
            request (Request): Request instance.
            pk (int): Showroom's pk.

        Returns:
            Response: HTTP 200 if has permissions otherwise 401/403.
        """

        showroom: ShowroomModel = self.get_object()
        serializer: ShowroomCarDiscountSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(showroom=showroom)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=['get'], detail=True, serializer_class=ShowroomCarDiscountSerializer)
    def get_discounts(self, request: Request, pk: int) -> Response:
        """
        get_statistics: Returns discounts of the showroom.

        Args:
            request (Request): Request instance.
            pk (int): Showroom's pk.

        Returns:
            Response: HTTP 200 if has permissions otherwise 401/403.
        """

        showroom: ShowroomModel = self.get_object()
        discounts: QuerySet = showroom.discounts.all()
        serializer: ShowroomHistorySerializer = self.get_serializer(discounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, serializer_class=ShowroomHistorySerializer)
    def get_statistics(self, request: Request, pk: int) -> Response:
        """
        get_statistics: Returns statistics for showrooms's operations.

        Args:
            request (Request): Request instance.
            pk (int): Showroom's pk.

        Returns:
            Response: HTTP 200 if has permissions otherwise 401/403.
        """

        showroom: ShowroomModel = self.get_object()
        history: QuerySet = showroom.history.all()
        serializer: ShowroomHistorySerializer = self.get_serializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, serializer_class=ShowroomCarSerializer)
    def get_cars(self, request: Request, pk: int) -> Response:
        """
        get_cars: Returns cars of the showroom.

        Args:
            request (Request): Request instance.
            pk (int): Showrooms's pk.

        Returns:
            Response: HTTP 200 if has permissions otherwise 401/403.
        """

        showroom: ShowroomModel = self.get_object()
        cars: QuerySet = showroom.cars.all()
        serializer: ShowroomCarSerializer = self.get_serializer(cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

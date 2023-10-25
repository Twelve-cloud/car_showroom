"""
views.py: File, containing views for a showroom application.
"""


from typing import ClassVar
from rest_framework import status, viewsets
from django.db.models.query import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from showroom.models import ShowroomModel
from showroom.services import ShowroomService
from showroom.serializers import (
    ShowroomSerializer,
    ShowroomHistorySerializer,
    ShowroomCarDiscountSerializer,
)


class ShowroomViewSet(viewsets.ModelViewSet):
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

    queryset: ClassVar[QuerySet[ShowroomModel]] = ShowroomModel.objects.all()

    serializer_class: ClassVar[type[ShowroomSerializer]] = ShowroomSerializer

    service: ClassVar[ShowroomService] = ShowroomService()

    permission_classes: ClassVar[list] = [IsAdminUser]

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        destroy: Instead of deleting from database this method set showrooms's is_active to False.

        Args:
            request (Request): Request instance.

        Returns:
            Response: HTTP 204 Response if showroom can be deleted otherwise HTTP 401/403.
        """

        self.service.delete_showroom(self.get_object())
        return Response(status=status.HTTP_204_NO_RESPONSE)

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
        history = showroom.history.all()
        serializer: ShowroomSerializer = self.get_serializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

        serializer: ShowroomCarDiscountSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_200_OK)

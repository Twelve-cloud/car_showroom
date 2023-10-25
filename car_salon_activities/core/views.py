"""
views.py: File, containing views for a core application.
"""


from rest_framework import mixins, status, viewsets
from django.db.models.query import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from core.models import CarModel
from core.services import CarService
from core.serializers import CarSerializer


class CarViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    """
    CarViewSet: Handling actions for a Car resource.
    Maps HTTP methods to actions:
        HEAD -> list
        HEAD -> retrieve
        GET -> list
        GET -> retrieve
        POST -> create
        DELETE -> destroy

    Args:
        viewsets.GenericViewSet (_type_): Builtin superclass for a CarViewset.
        mixins.CreateModelMixin (_type_): Builtin superclass for a CarViewset.
        mixins.ListModelMixin (_type_): Builtin superclass for a CarViewset.
        mixins.RetrieveModelMixin (_type_): Builtin superclass for a CarViewset.
        mixins.DestroyModelMixin (_type_): Builtin superclass for a CarViewset.
    """

    serializer_class = CarSerializer

    permission_classes = [IsAdminUser]

    service = CarService()

    def get_queryset(self) -> QuerySet:
        """
        get_queryset: Returns all active car objects.

        Returns:
            QuerySet: Queryset of all active car objects.
        """

        return CarModel.objects.filter(is_active=True)

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        destroy: Instead of deleting from database this method set car's is_active field to False.

        Args:
            request (Request): Request instance.

        Returns:
            Response: HTTP 204 Response.
        """

        self.service.set_car_as_inactive(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

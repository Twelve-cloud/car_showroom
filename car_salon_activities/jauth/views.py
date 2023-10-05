"""
views.py: File, containing views for an jauth application.
"""


from rest_framework import viewsets
from django.db.models.query import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from jauth.models import User
from jauth.permissions import IsUserOwner
from jauth.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    UserViewSet: Handling every action for an User resource.
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
        viewsets.ModelViewSet (_type_): Builtin superclass for an UserViewSet.
    """

    queryset: QuerySet[User] = User.objects.all()
    serializer_class: type[UserSerializer] = UserSerializer
    permission_map: dict = {
        'create': [
            ~IsAuthenticated | IsAdminUser,
        ],
        'list': [
            IsAuthenticated,
        ],
        'retrieve': [
            IsAuthenticated,
        ],
        'update': [
            IsAuthenticated & IsUserOwner,
        ],
        'partial_update': [
            IsAuthenticated & IsUserOwner,
        ],
        'destroy': [
            IsAuthenticated & (IsUserOwner | IsAdminUser),
        ],
    }

    def get_permissions(self) -> list:
        self.permission_classes = self.permission_map.get(self.action, [])
        return super().get_permissions()

    def create(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().create(request, *args, **kwargs)

    def update(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().update(request, *args, **kwargs)

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().destroy(request, *args, **kwargs)

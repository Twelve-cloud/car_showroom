"""
views.py: File, containing views for an jauth application.
"""


from rest_framework.permissions import IsAdminUser, IsAuthenticated
from jauth.services import generate_token_pair, get_payload_by_token
from jauth.serializers import UserSerializer, TokenSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.query import QuerySet
from rest_framework.request import Request
from jauth.permissions import IsUserOwner
from rest_framework import viewsets
from rest_framework import status
from jauth.models import User


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


class TokenViewSet(viewsets.GenericViewSet):
    serializer_class = TokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = generate_token_pair(user_id=serializer.validated_data['id'])
        return Response(tokens, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def refresh(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh', None)

        if refresh_token is None:
            return Response(
                data={'Refresh Token': 'Not specified'},
                status=status.HTTP_400_BAD_REQUEST
            )

        payload = get_payload_by_token(token=refresh_token)

        if payload is None:
            return Response(
                data={'Refresh Token': 'Expired'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(pk=payload.get('sub'))
        tokens = generate_token_pair(user_id=user.id)

        return Response(tokens, status=status.HTTP_200_OK)

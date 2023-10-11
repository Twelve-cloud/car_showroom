"""
views.py: File, containing views for a jauth application.
"""


from typing import ClassVar
from rest_framework import status, viewsets
from django.db.models.query import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from jauth.models import User
from jauth.permissions import IsUserOwner
from jauth.serializers import UserSerializer, AccessTokenSerializer, RefreshTokenSerializer
from jauth.services import send_verification_link, confirm_email
from rest_framework.reverse import reverse


class UserViewSet(viewsets.ModelViewSet):
    """
    UserViewSet: Handling every action for a User resource.
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
        viewsets.ModelViewSet (_type_): Builtin superclass for a UserViewSet.
    """

    queryset: ClassVar[QuerySet[User]] = User.objects.all()
    serializer_class: ClassVar[type[UserSerializer]] = UserSerializer
    permission_map: ClassVar[dict] = {
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
            IsAuthenticated,
        ],
        'partial_update': [
            IsAuthenticated,
        ],
        'destroy': [
            IsAuthenticated & (IsUserOwner | IsAdminUser),
        ],
    }

    def get_permissions(self) -> list:
        self.permission_classes = self.permission_map.get(self.action, [])
        return super().get_permissions()

    def create(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        link = reverse('jauth:user-email-confirmation', request=request)
        send_verification_link(link, request.data['email'])
        return super().create(request, *args, **kwargs)

    def update(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        if 'password' or 'email' in request.data:
            link = reverse('jauth:user-email-confirmation', request=request)
            send_verification_link(link, request.user.email)
        return super().update(request, *args, **kwargs)

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods='get')
    def email_confirmation(self, request):
        user_token = request.query_params.get('token', None)
        is_confirmed = confirm_email(user_token)

        if not is_confirmed:
            return Response(
                {'Verification status': 'Verified'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {'Verification status': 'Verified'},
            status=status.HTTP_200_OK,
        )


class TokenViewSet(viewsets.GenericViewSet):
    """
    TokenViewSet: Hadling token creation.

    Args:
        viewsets.GenericViewSet (_type_): Builtin superclass for an TokenViewSet.
    """

    permission_classes: ClassVar[list] = [~IsAuthenticated]
    serializer_map: ClassVar[dict] = {
        'create': AccessTokenSerializer,
        'refresh': RefreshTokenSerializer,
    }

    def get_serializer_class(self) -> AccessTokenSerializer | RefreshTokenSerializer:
        return self.serializer_map.get(self.action, None)

    def create(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def refresh(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

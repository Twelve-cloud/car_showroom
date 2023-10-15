"""
views.py: File, containing views for a jauth application.
"""


from typing import ClassVar, Optional
from rest_framework import status, viewsets
from django.db.models.query import QuerySet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from jauth.models import User
from jauth.services import UserService
from jauth.permissions import IsUserOwner
from jauth.serializers import (
    UserSerializer,
    AccessTokenSerializer,
    RefreshTokenSerializer,
    ResetPasswordSerializer,
)


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

    service: UserService = UserService()
    queryset: ClassVar[QuerySet[User]] = User.objects.all()
    serializer_class: ClassVar[type[UserSerializer]] = UserSerializer
    filter_backends: list = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]
    filterset_fields: list = [
        'email',
        'username',
        'first_name',
        'last_name',
    ]
    search_fields: list = [
        'email',
        'username',
        'first_name',
        'last_name',
    ]
    ordering_fields: list = [
        'email',
        'username',
        'first_name',
        'last_name',
    ]
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
            IsAuthenticated & IsUserOwner,
        ],
        'partial_update': [
            IsAuthenticated & IsUserOwner,
        ],
        'destroy': [
            IsAuthenticated & (IsUserOwner | IsAdminUser),
        ],
        'confirm_email': [
            ~IsAuthenticated,
        ],
        'reset_password': [
            ~IsAuthenticated,
        ],
        'reset_password_confirm': [
            ~IsAuthenticated,
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
        create: Creates user account and sends confirmation link to user's email address.

        Args:
            request (Request): Request instance.

        Returns:
            Response: HTTP 201 Reponse if user can be created otherwise HTTP 400.
        """

        response: Response = super().create(request, *args, **kwargs)
        self.service.send_confirmation_link(response.data.get('email'))
        return response

    def update(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        update: Updates user account and if email is specified then sends link to confirm email.

        Args:
            request (Request): Request instance.

        Returns:
            Response: Updated user json if user can be updated otherwise HTTP 400.
        """

        response: Response = super().update(request, *args, **kwargs)

        if 'email' in request.data:
            user: User = self.get_object()
            self.service.set_user_as_not_verified(user)
            self.service.send_confirmation_link(user.email)

        return response

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        destroy: Instead of deleting from database this method set user's is_active field to False.

        Args:
            request (Request): Request instance.

        Returns:
            Response: HTTP 204 Response if user can be deleted otherwise HTTP 400.
        """

        self.service.set_user_as_inactive(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, url_path=r'confirm_email/(?P<token>[\S-]+)')
    def confirm_email(self, request: Request, token: str) -> Response:
        """
        confirm_email: Checks confirmation token and if it is correct makes account verified.

        Args:
            request (Request): Request instance.

        Returns:
            Response: HTTP 400 if token is not valid otherwise HTTP 200 Response.
        """

        user: Optional[User] = self.service.get_user_by_token(token)

        if user is None:
            return Response({'Error': 'Bad link'}, status=status.HTTP_400_BAD_REQUEST)

        self.service.set_user_as_verified(user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path=r'reset_password/(?P<email>[\S-]+)')
    def reset_password(self, request: Request, email: str) -> Response:
        """
        reset_password: Sends link to email address to reset password.

        Args:
            request (Request): Request insatnce.
            email (str): Email of the user.

        Returns:
            Response: Response insatnce.
        """

        user: Optional[User] = self.service.get_user_by_email(email)

        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.service.send_reset_password_link(user.email)
        return Response(status=status.HTTP_200_OK)

    @action(
        methods=['patch'],
        detail=False,
        serializer_class=ResetPasswordSerializer,
        url_path=r'reset_password_confirm/(?P<token>[\S-]+)',
    )
    def reset_password_confirm(self, request: Request, token: str) -> Response:
        """
        reset_password_confirm: Checks confirmation token and if it is correct, then changes pass.

        Args:
            request (Request): Request instance.
            token (str): Confirmation token.

        Returns:
            Response: Reponse instance.
        """

        user: Optional[User] = self.service.get_user_by_token(token)

        if user is None:
            return Response({'Error': 'Bad link'}, status=status.HTTP_400_BAD_REQUEST)

        serializer: ResetPasswordSerializer = self.get_serializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)


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
        """
        get_serializer_class: Returns proper serializer class according to an action.

        Returns:
            AccessTokenSerializer | RefreshTokenSerializer: Serializer class.
        """

        return self.serializer_map.get(self.action, None)

    def create(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        create: Creates new pair of token: access and refresh.

        Args:
            request (Request): Request instance.

        Returns:
            Response: Response instance.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def refresh(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        refresh: Creates new pair of token: access and refresh when access token is expired.

        Args:
            request (Request): Request instance.


        Returns:
            Response: Response instance.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

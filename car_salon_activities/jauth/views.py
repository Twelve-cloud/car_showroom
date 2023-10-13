"""
views.py: File, containing views for a jauth application.
"""


from typing import ClassVar
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
from jauth.serializers import UserSerializer, AccessTokenSerializer, RefreshTokenSerializer


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
        'verify_email': [
            ~IsAuthenticated,
        ],
    }

    def get_permissions(self) -> list:
        """
        get_permissions: Returns apropriate permission classes according to action.

        Returns:
            list: Permission classes.
        """

        self.permission_classes = self.permission_map.get(self.action, [])
        return super().get_permissions()

    def create(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        create: Creates user account and sends verification link to user's email address.

        Args:
            request (Request): Request instance.

        Returns:
            Response: Everytime HTTP 201 Response.
        """

        response = super().create(request, *args, **kwargs)
        self.service.send_verification_link(response.data.get('email'))
        return response

    def update(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().update(request, *args, **kwargs)

    def destroy(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        destroy: Instead of deleting from database this method set user's is_active field to False.

        Args:
            request (Request): Request instance.

        Returns:
            Response: Everytime HTTP 204 Response.
        """

        self.service.set_user_as_inactive(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False)
    def verify_email(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        """
        verify_email: Checks verification token and if it is correct verifies user.

        Args:
            request (Request): Request instance.

        Returns:
            Response: HTTP 400 if token is not valid otherwise HTTP 200 Response.
        """

        verification_token = request.data.get('token', None)
        user = self.service.get_user_by_token(verification_token)

        if user is None:
            return Response({'Error': 'Bad link'}, status=status.HTTP_400_BAD_REQUEST)

        self.service.set_user_as_active(user)

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

        serializer = self.get_serializer_class()(data=request.data)
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

        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

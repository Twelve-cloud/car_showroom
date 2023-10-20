"""
views.py: File, containing views for an jauth application.
"""


from typing import Any, ClassVar, Iterable, Optional
from rest_framework import status, viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from jauth.swagger import (
    user_list_schema_extenstion,
    user_update_schema_extension,
    user_create_schema_extenstion,
    token_create_schema_extenstion,
    user_destroy_schema_extenstion,
    token_refresh_schema_extenstion,
    user_retrieve_schema_extenstion,
    user_confirm_email_schema_extenstion,
    user_partial_update_schema_extenstion,
    user_reset_password_schema_extenstion,
    user_reset_password_confirm_schema_extenstion,
)
from jauth.permissions import IsUserOwner
from jauth.serializers import (
    UserSerializer,
    EmailSerializer,
    PasswordSerializer,
    AccessTokenSerializer,
    RefreshTokenSerializer,
)
from jauth.services.user_service import UserDTO, UserService
from jauth.services.user_auth_service import TokenPairDTO, CredentialsDTO, UserAuthService
from jauth.services.user_mail_service import (
    EmailDTO,
    PasswordDTO,
    UserMailService,
    ConfirmationTokenDTO,
)


@extend_schema(tags=['User'])
@extend_schema_view(
    list=extend_schema(**user_list_schema_extenstion),
    update=extend_schema(**user_update_schema_extension),
    create=extend_schema(**user_create_schema_extenstion),
    destroy=extend_schema(**user_destroy_schema_extenstion),
    retrieve=extend_schema(**user_retrieve_schema_extenstion),
    confirm_email=extend_schema(**user_confirm_email_schema_extenstion),
    partial_update=extend_schema(**user_partial_update_schema_extenstion),
    reset_password=extend_schema(**user_reset_password_schema_extenstion),
    reset_password_confirm=extend_schema(**user_reset_password_confirm_schema_extenstion),
)
class UserViewSet(viewsets.ViewSet):
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
        viewsets.ViewSet (_type_): Builtin superclass for a UserViewSet.
    """

    user_service: ClassVar[UserService] = UserService()
    user_mail_service: ClassVar[UserMailService] = UserMailService()

    permission_map: dict[str, Any] = {
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

    def get_permissions(self) -> list[Any]:
        """
        get_permissions: Return apropriate permission classes according to action.

        Returns:
            list: Permission classes.
        """

        self.permission_classes: list[Any] = self.permission_map.get(self.action, [])
        return super().get_permissions()

    def _make_user_dto_from_val_data(self, data: dict) -> UserDTO:
        """
        _make_user_dto_from_val_data: Make UserDTO from validated data.

        Args:
            data (dict): Validated data.

        Returns:
            UserDTO: UserDTO.
        """

        return UserDTO(
            username=data.get('username', None),
            email=data.get('email', None),
            password=data.get('password', None),
            first_name=data.get('first_name', None),
            last_name=data.get('last_name', None),
        )

    def _prepare_user(self, dto: UserDTO) -> dict[str, Any]:
        """
        _prepare_user: Make user dict from UserDTO.

        Args:
            user_dto (UserDTO): UserDTO.

        Returns:
            dict[str, Any]: User dict object.
        """

        return {
            'pk': dto.pk,
            'username': dto.username,
            'email': dto.email,
            'password': dto.password,
            'first_name': dto.first_name,
            'last_name': dto.last_name,
            'date_joined': dto.date_joined,
            'last_updated': dto.last_updated,
            'last_login': dto.last_login,
            'is_active': dto.is_active,
            'is_staff': dto.is_staff,
            'is_verified': dto.is_verified,
        }

    def _make_email_dto_from_val_data(self, data: dict) -> EmailDTO:
        """
        _make_email_dto_from_val_data: Make EmailDTO from validated data.

        Args:
            data (dict): Validated data.

        Returns:
            EmailDTO: EmailDTO.
        """

        return EmailDTO(
            email=data['email'],
        )

    def _make_passw_dto_from_val_data(self, data: dict) -> PasswordDTO:
        """
        _make_passw_dto_from_val_data: Make PasswordDTO from validated data.

        Args:
            data (dict): Validated data.

        Returns:
            PasswordDTO: PasswordDTO.
        """

        return PasswordDTO(
            password=data['password'],
        )

    def _make_confirmation_token_dto(self, token: str) -> ConfirmationTokenDTO:
        """
        _make_confirmation_token_dto: Make ConfirmationTokenDTO from token str.

        Args:
            token (str): Token str.

        Returns:
            ConfirmationTokenDTO: ConfirmationTokenDTO.
        """

        return ConfirmationTokenDTO(
            token=token,
        )

    def create(self, request: Request) -> Response:
        """
        create: Creates user account and sends confirmation link to user's email address.

        Args:
            request (Request): Request instance.

        Returns:
            Response: HTTP 201 Reponse if user can be created otherwise HTTP 400.
        """

        serializer: UserSerializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_dto: UserDTO = self._make_user_dto_from_val_data(serializer.validated_data)
        created_user_dto = self.user_service.create(user_dto)

        email_dto: EmailDTO = self._make_email_dto_from_val_data(serializer.validated_data)
        self.user_mail_service.send_confirmation_link(email_dto)

        created_user = self._prepare_user(created_user_dto)

        return Response(data=created_user, status=status.HTTP_201_CREATED)

    def list(self, request: Request) -> Response:
        """
        list: Return all users.

        Args:
            request (Request): Request instance.

        Returns:
            Response: List of users in json format.
        """

        user_dto_list: Iterable[UserDTO] = self.user_service.get_all()
        serializer: UserSerializer = UserSerializer(user_dto_list, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request: Request, pk: int) -> Response:
        """
        retrieve: Return information about concrete user.

        Args:
            request (Request): Request instance.
            pk (int): id of the current user.

        Returns:
            Response: Information about concrete user.
        """

        user_dto: UserDTO = self.user_service.get_by_pk(pk)
        serializer: UserSerializer = UserSerializer(user_dto)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, pk: int, partial: bool = False) -> Response:
        """
        update: Update existing user account (fully).
        If email is specified, it also sends email confirmation link to specified email address.
        Also if email is being updated, then user will be marked as unverified.
        When email address if confirmed, user account will be verified.

        Args:
            request (Request): Request instance.
            pk (int): id of the current user.
            partial (bool, optional): If false then HTTP method is PUT, otherwise PATCH.

        Returns:
            Response: Updated user information in json format.
        """

        user_dto: UserDTO = self.user_service.get_by_pk(pk)
        self.check_object_permissions(request, user_dto)

        serializer: UserSerializer = UserSerializer(user_dto, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        new_user_dto: UserDTO = self._make_user_dto_from_val_data(serializer.validated_data)
        updated_user_dto = self.user_service.update(pk, new_user_dto)

        if 'email' in serializer.validated_data:
            email_dto: EmailDTO = self._make_email_dto_from_val_data(serializer.validated_data)
            self.user_service.make_user_unferified(pk)
            self.user_mail_service.send_confirmation_link(email_dto)

        updated_user = self._prepare_user(updated_user_dto)

        return Response(data=updated_user, status=status.HTTP_200_OK)

    def partial_update(self, request: Request, pk: int) -> Response:
        """
        update: Update existing user account (partially).
        If email is specified, it also sends email confirmation link to specified email address.
        Also if email is being updated, then user will be marked as unverified.
        When email address if confirmed, user account will be verified.

        Args:
            request (Request): Request instance.
            pk (int): id of the current user.

        Returns:
            Response: Updated user information in json format.
        """

        return self.update(request, pk, True)

    def destroy(self, request: Request, pk: int) -> Response:
        """
        destroy: Deactivates user account. Marks user as inactive instead of deleting from database.

        Args:
            request (Request): Request instance.
            pk (int): id of the current user.

        Returns:
            Response: HTTP 204 status.
        """

        user_dto: UserDTO = self.user_service.get_by_pk(pk)
        self.check_object_permissions(request, user_dto)
        self.user_service.destroy(pk)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, url_path=r'confirm_email/(?P<token>[\S-]+)')
    def confirm_email(self, request: Request, token: str) -> Response:
        """
        confirm_email: Checks confirmation token and if it is correct makes account verified.

        Args:
            request (Request): Request instance.
            token (str): Token.

        Returns:
            Response: HTTP 400 if token is not valid otherwise HTTP 200 Response.
        """

        token_dto: ConfirmationTokenDTO = self._make_confirmation_token_dto(token)
        self.user_mail_service.set_user_as_verified(token_dto)

        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def reset_password(self, request: Request) -> Response:
        """
        reset_password: Sends link to email address to reset password.

        Args:
            request (Request): Request insatnce.

        Returns:
            Response: Response insatnce.
        """

        serializer: EmailSerializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email_dto: EmailDTO = self._make_email_dto_from_val_data(serializer.validated_data)
        self.user_mail_service.send_reset_password_link(email_dto)

        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path=r'reset_password_confirm/(?P<token>[\S-]+)')
    def reset_password_confirm(self, request: Request, token: str) -> Response:
        """
        reset_password_confirm: Checks confirmation token and if it is correct, then changes pass.

        Args:
            request (Request): Request instance.
            token (str): Confirmation token.

        Returns:
            Response: Reponse instance.
        """

        serializer: PasswordSerializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_dto: ConfirmationTokenDTO = self._make_confirmation_token_dto(token)
        passw_dto: PasswordDTO = self._make_passw_dto_from_val_data(serializer.validated_data)
        self.user_mail_service.reset_user_password(token_dto, passw_dto)

        return Response(status=status.HTTP_200_OK)


@extend_schema(tags=['Token'])
@extend_schema_view(
    create=extend_schema(**token_create_schema_extenstion),
    refresh=extend_schema(**token_refresh_schema_extenstion),
)
class TokenViewSet(viewsets.ViewSet):
    """
    TokenViewSet: Hadling token creation.

    Args:
        viewsets.GenericViewSet (_type_): Builtin superclass for an TokenViewSet.
    """

    user_auth_service: ClassVar[UserAuthService] = UserAuthService()
    permission_classes: ClassVar[list[Any]] = [~IsAuthenticated]

    def _prepare_tokens(self, dto: TokenPairDTO) -> dict[str, Optional[str]]:
        """
        _prepare_tokens: Make token pair dict from TokenPairDTO.

        Args:
            dto (TokenPairDTO): TokenPairDTO.

        Returns:
            dict[str, Optional[str]]: Token pair dict object.
        """

        return {
            'access': dto.access,
            'refresh': dto.refresh,
        }

    def _make_creds_dto_from_val_data(self, data: dict) -> CredentialsDTO:
        """
        _make_creds_dto_from_val_data: Make CredentialsDTO from validated data.

        Args:
            data (dict): Validated data.

        Returns:
            CredentialsDTO: CredentialsDTO.
        """

        return CredentialsDTO(
            email=data['email'],
            password=data['password'],
        )

    def _make_token_pair_dto_from_val_data(self, data: dict) -> TokenPairDTO:
        """
        _make_token_pair_dto_from_val_data: Make TokenPairDTO from validated data.

        Args:
            data (dict): Validated data.

        Returns:
            TokenPairDTO: TokenPairDTO.
        """

        return TokenPairDTO(
            access=data.get('access', None),
            refresh=data.get('refresh', None),
        )

    def create(self, request: Request) -> Response:
        """
        create: Creates new pair of token: access and refresh.

        Args:
            request (Request): Request instance.

        Returns:
            Response: New token pair in json format.
        """

        serializer: AccessTokenSerializer = AccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        creds_dto: CredentialsDTO = self._make_creds_dto_from_val_data(serializer.validated_data)
        token_pair_dto: TokenPairDTO = self.user_auth_service.get_tokens(creds_dto)
        tokens: dict[str, Optional[str]] = self._prepare_tokens(token_pair_dto)

        return Response(tokens, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def refresh(self, request: Request) -> Response:
        """
        refresh: Creates new pair of token: access and refresh when access token is expired.

        Args:
            request (Request): Request instance.

        Returns:
            Response: New token pair in json format.
        """

        serializer: RefreshTokenSerializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dto: TokenPairDTO = self._make_token_pair_dto_from_val_data(serializer.validated_data)
        token_pair_dto: TokenPairDTO = self.user_auth_service.refresh(dto)
        tokens: dict[str, Optional[str]] = self._prepare_tokens(token_pair_dto)

        return Response(tokens, status=status.HTTP_200_OK)

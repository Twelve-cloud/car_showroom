"""
serializers.py: File, containing serializers for a jauth application.
"""


from typing import ClassVar, Optional
from rest_framework import serializers
from jauth.models import User
from jauth.tokens import Token


class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer: Serializes user json to py-native types and vice versa.

    Args:
        serializers.ModelSerializer (_type_): Builtin superclass for a UserSerliazer.
    """

    def create(self, validated_data: dict) -> User:
        """
        create: Creates user object.

        Args:
            validated_data (dict): Validated data.

        Returns:
            User: User instance.
        """

        created_user = super().create(validated_data)
        created_user.set_password(created_user.password)

        return created_user

    def update(self, instance: User, validated_data: dict) -> User:
        """
        update: Updates user object.

        Args:
            instance (User): User instance.
            validated_data (dict): Validated data.

        Returns:
            User: User instance.
        """

        password = validated_data.pop('password', None)

        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)

    class Meta:
        model: ClassVar[type[User]] = User

        fields: ClassVar[list] = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'date_joined',
            'last_updated',
            'last_login',
            'is_active',
            'is_staff',
            'is_verified',
        ]

        read_only_fields: ClassVar[list] = [
            'date_joined',
            'last_updated',
            'last_login',
            'is_active',
            'is_staff',
            'is_verified',
        ]


class AccessTokenSerializer(serializers.Serializer):
    """
    AccessTokenSerializer: Serializes token form to py-native types and vice versa.

    Args:
        serializers.Serializer (_type_): Builtin superclass for an AccessTokenSerializer.

    Raises:
        serializers.ValidationError: Raises when email adress is not specified.
        serializers.ValidationError: Raises when password is not specified.
        serializers.ValidationError: Raises when spicified email adress is not found.
        serializers.ValidationError: Raises when spicified password is not correct.
        serializers.ValidationError: Raises when account is deactivated.
    """

    token_class: ClassVar[type[Token]] = Token

    email = serializers.CharField(
        max_length=320,
        min_length=3,
        write_only=True,
    )

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

    def validate(self, data: dict) -> dict:
        """
        validate: Validates request data.

        Args:
            data (dict): Incoming data.

        Raises:
            serializers.ValidationError: Raises when email adress is not specified.
            serializers.ValidationError: Raises when password is not specified.
            serializers.ValidationError: Raises when spicified email adress is not found.
            serializers.ValidationError: Raises when spicified password is not correct.
            serializers.ValidationError: Raises when account is not verified.

        Returns:
            dict: Dict with new access token and refresh token.
        """

        email: str = data['email']

        password: str = data['password']

        user: Optional[User] = User.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError(
                'A user with this email is not found.',
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                'Password is not correct.',
            )

        if not user.is_active and not user.is_verified:
            raise serializers.ValidationError(
                'Account is not virified.',
            )

        if not user.is_active and user.is_verified:
            user.set_active()

        user.set_last_login()

        access_token, refresh_token = self.token_class.for_user(user)

        return {
            'access': access_token.token,
            'refresh': refresh_token.token,
        }


class RefreshTokenSerializer(serializers.Serializer):
    """
    RefreshTokenSerializer: Serializes refresh-token form to py-native types and vice versa.

    Args:
        serializers.Serializer (_type_): Builtin superclass for an RefreshTokenSerializer.

    Raises:
        serializers.ValidationError: Raises when refresh token is not specified.
        serializers.ValidationError: Raises when refresh token is expired.
        serializers.ValidationError: Raises when refresh token is invalid.
        serializers.ValidationError: Raises when refresh token is not correct.
    """

    token_class: ClassVar[type[Token]] = Token

    refresh = serializers.CharField(
        max_length=128,
        min_length=32,
        write_only=True,
    )

    def validate(self, data: dict) -> dict:
        """
        validate: Validates request data.

        Args:
            data (dict): Incoming data.

        Raises:
            serializers.ValidationError: Raises when refresh token is not specified.
            serializers.ValidationError: Raises when refresh token is expired.
            serializers.ValidationError: Raises when refresh token is invalid.
            serializers.ValidationError: Raises when refresh token is not correct.

        Returns:
            dict: Dict with new access token and refresh token.
        """

        user_refresh_token: str = data['refresh']

        token: Token = self.token_class(token=user_refresh_token, type='refresh')

        is_verified: Optional[bool] = token.verify()

        if not is_verified:
            if token.expired:
                raise serializers.ValidationError(
                    'Token is expired.',
                )

            raise serializers.ValidationError(
                'Token is invalid.',
            )

        user: Optional[User] = token.get_user_by_token()

        if user is None:
            raise serializers.ValidationError(
                'Token is not correct.',
            )

        user.set_last_login()

        access_token, refresh_token = self.token_class.for_user(user)

        return {
            'access': access_token.token,
            'refresh': refresh_token.token,
        }

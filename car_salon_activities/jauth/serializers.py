"""
serializers.py: File, containing serializers for an jauth application.
"""


from typing import ClassVar
from rest_framework import serializers
from jauth.models import User
from jauth.tokens import Token


class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer: Serializes User object to py-native types and vice versa.

    Args:
        serializers.ModelSerializer (_type_): Builtin superclass for an UserSerliazer.
    """

    class Meta:
        model: ClassVar[type[User]] = User
        fields: ClassVar[tuple] = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'date_joined',
            'last_login',
            'is_active',
            'is_staff',
        )
        read_only_fields: ClassVar[tuple] = (
            'date_joined',
            'last_login',
            'is_active',
            'is_staff',
        )


class AccessTokenSerializer(serializers.Serializer):
    token_class = Token

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

    def validate(self, data: dict) -> None:
        email = data.get('email', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required.',
            )

        password = data.get('password', None)

        if password is None:
            raise serializers.ValidationError(
                'A password is required.',
            )

        user = User.objects.filter(email=email).first()

        if user is None:
            raise serializers.ValidationError(
                'A user with this email is not found.',
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                'Password is not correct.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'Account is deactivated.',
            )

        token = self.token_class.for_user(user)

        return {
            'refresh': token.refresh_token,
            'access': token.access_token,
        }


class RefreshTokenSerializer(serializers.Serializer):
    token_class = Token

    refresh = serializers.CharField(
        max_length=128,
        min_length=32,
        write_only=True,
    )

    def validate(self, data):
        refresh_token = data.get('refresh', None)

        if refresh_token is None:
            raise serializers.ValidationError(
                'Refresh token is required.',
            )

        is_verified = self.token_class.verify_token(token=refresh_token)

        if not is_verified:
            raise serializers.ValidationError(
                'Refresh token is expired.',
            )

        user = self.token_class.get_user_by_token(token=refresh_token)

        if user is None:
            raise serializers.ValidationError(
                'Refresh token is incorrect.',
            )

        token = self.token_class.for_user(user)

        return {
            'refresh': token.refresh_token,
            'access': token.access_token,
        }

"""
serializers.py: File, containing serializers for an jauth application.
"""


from typing import ClassVar
from rest_framework import serializers
from jauth.models import User


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


class TokenSerializer(serializers.Serializer):
    """
    SignInSerializer: Serializes email and password to py-native types and vice versa.

    Args:
        serializers.Serializer (_type_): Builtin superclass for an AuthSerliazer.

    Raises:
        serializers.ValidationError: Email is not provided.
        serializers.ValidationError: Password is not provided.
        serializers.ValidationError: User is not found.
    """

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

        return {'id': user.id}

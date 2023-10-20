"""
serializers.py: File, containing serializers for an jauth application.
"""


from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from jauth.models import User


class UserSerializer(serializers.Serializer):
    """
    UserSerializer: Serialize user json to py-native types or user class to py-native types.

    Args:
        serializers.Serializer (_type_): Builtin superclass for a UserSerliazer.
    """

    pk = serializers.IntegerField(
        label='ID',
        read_only=True,
    )

    username = serializers.CharField(
        max_length=32,
        min_length=8,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    email = serializers.EmailField(
        max_length=320,
        min_length=3,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        max_length=128,
        min_length=8,
    )

    first_name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        max_length=32,
        required=False,
    )

    last_name = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        max_length=32,
        required=False,
    )

    date_joined = serializers.DateTimeField(
        read_only=True,
    )

    last_updated = serializers.DateTimeField(
        read_only=True,
    )

    last_login = serializers.DateTimeField(
        allow_null=True,
        read_only=True,
    )

    is_active = serializers.BooleanField(
        read_only=True,
    )

    is_staff = serializers.BooleanField(
        read_only=True,
    )

    is_verified = serializers.BooleanField(
        read_only=True,
    )


class EmailSerializer(serializers.Serializer):
    """
    EmailSerializer: Serialize email json to py-native types to py-native types.

    Args:
        serializers.Serializer (_type_): Builtin superclass for a UserSerliazer.
    """

    email = serializers.EmailField(
        max_length=320,
        min_length=3,
        write_only=True,
    )


class PasswordSerializer(serializers.Serializer):
    """
    PasswordSerializer: Serialize password json to py-native types to py-native types.

    Args:
        serializers.Serializer (_type_): Builtin superclass for a UserSerliazer.
    """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )


class AccessTokenSerializer(serializers.Serializer):
    """
    AccessTokenSerializerSerializer: Serialize credentials to py-native types to py-native types.

    Args:
        serializers.Serializer (_type_): Builtin superclass for a UserSerliazer.
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


class RefreshTokenSerializer(serializers.Serializer):
    """
    RefreshTokenSerializer: Serialize refresh token json to py-native types to py-native types.

    Args:
        serializers.Serializer (_type_): Builtin superclass for a UserSerliazer.
    """

    refresh = serializers.CharField(
        max_length=128,
        min_length=32,
        write_only=True,
    )

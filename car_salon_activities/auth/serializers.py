"""
serializers.py: File, containing serializers for an auth application.
"""


from typing import ClassVar

from rest_framework import serializers

from auth.models import User


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

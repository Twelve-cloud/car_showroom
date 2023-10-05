from rest_framework import serializers
from auth.models import User


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'last_login',
        )
        read_only_fields = (
            'username',
            'first_name',
            'last_name',
            'last_login',
        )


class FullUserSerializer(BasicUserSerializer):
    class Meta:
        model = User
        fields = (
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
        read_only_fields = (
            'date_joined',
            'last_login',
            'is_active',
            'is_staff',
        )

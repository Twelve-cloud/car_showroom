"""
serializers.py: File, containing serializers for a core application.
"""


from typing import ClassVar
from rest_framework import serializers
from core.models import CarModel


class CarSerializer(serializers.ModelSerializer):
    """
    CarSerializer: Serializes car json to py-native types and vice versa.

    Args:
        serializers.ModelSerializer (_type_): Builtin superclass for a CarSerliazer.
    """

    class Meta:
        model: ClassVar[type[CarModel]] = CarModel

        fields: list = [
            'created_at',
            'last_updated',
            'is_active',
            'brand',
            'transmission_type',
            'creation_year',
            'miliage',
        ]

        read_only_fields: list = [
            'created_at',
            'last_updated',
            'is_active',
        ]

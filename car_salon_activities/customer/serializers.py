"""
serializers.py: File, containing serializers for a customer application.
"""


from typing import ClassVar
from rest_framework import serializers
from customer.models import CustomerModel, CustomerHistory


class CustomerSerializer(serializers.ModelSerializer):
    """
    CustomerSerializer: Serializes customer json to py-native types and vice versa.

    Args:
        serializers.ModelSerializer (_type_): Builtin superclass for a CarSerliazer.
    """

    class Meta:
        model: ClassVar[type[CustomerModel]] = CustomerModel

        fields: list = [
            'created_at',
            'last_updated',
            'is_active',
            'balance',
        ]

        read_only_fields: list = [
            'created_at',
            'last_updated',
            'is_active',
        ]


class CustomerHistorySerializer(serializers.ModelSerializer):
    """
    CustomerHistorySerializer: Serializes customer history json to py-native types and vice versa.

    Args:
        serializers.ModelSerializer (_type_): Builtin superclass for a CarSerliazer.
    """

    class Meta:
        model: ClassVar[type[CustomerModel]] = CustomerHistory

        fields: list = [
            'created_at',
            'last_updated',
            'is_active',
            'customer',
            'car',
            'purchase_price',
            'showroom',
        ]

        read_only_fields: list = [
            'created_at',
            'last_updated',
            'is_active',
            'customer',
            'car',
            'purchase_price',
            'showroom',
        ]

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
        serializers.ModelSerializer (_type_): Builtin superclass for a CustomerSerializer.
    """

    class Meta:
        model: ClassVar[type[CustomerModel]] = CustomerModel

        fields: ClassVar[list] = [
            'created_at',
            'last_updated',
            'is_active',
            'balance',
        ]

        read_only_fields: ClassVar[list] = [
            'created_at',
            'last_updated',
            'is_active',
        ]


class CustomerHistorySerializer(serializers.ModelSerializer):
    """
    CustomerHistorySerializer: Serializes customer history json to py-native types and vice versa.

    Args:
        serializers.ModelSerializer (_type_): Builtin superclass for a CustomerHistorySerializer.
    """

    class Meta:
        model: ClassVar[type[CustomerModel]] = CustomerHistory

        fields: ClassVar[list] = [
            'created_at',
            'last_updated',
            'is_active',
            'customer',
            'car',
            'purchase_price',
            'showroom',
        ]

        read_only_fields: ClassVar[list] = [
            'created_at',
            'last_updated',
            'is_active',
            'customer',
            'car',
            'purchase_price',
            'showroom',
        ]

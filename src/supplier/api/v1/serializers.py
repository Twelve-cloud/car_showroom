"""
serializers.py: File, containing serializers for a supplier application.
"""


from typing import ClassVar
from rest_framework import serializers
from supplier.models import SupplierCar, SupplierModel, SupplierHistory, SupplierCarDiscount


class SupplierSerializer(serializers.ModelSerializer):
    """
    SupplierSerializer: Serializes supplier json to py-native types and vice versa.

    Args:
        serializers.ModelSerializer (_type_): Builtin superclass for a SupplierSerliazer.
    """

    class Meta:
        model: ClassVar[type[SupplierModel]] = SupplierModel

        fields: ClassVar[list] = [
            'created_at',
            'last_updated',
            'is_active',
            'name',
            'creation_year',
            'customers_count',
            'number_of_sales',
            'discount_for_unique_customers',
            'showrooms',
            'cars',
        ]

        read_only_fields: ClassVar[list] = [
            'created_at',
            'last_updated',
            'is_active',
            'customers_count',
            'showrooms',
            'cars',
        ]


class SupplierCarDiscountSerializer(serializers.ModelSerializer):
    """
    SupplierCarDiscountSerializer: Serializes supplier discount json to native types and vice versa.

    Args:
        serializers.ModelSerializer (_type_): Builtin supclass for a SupplierCarDiscountSerializer.
    """

    class Meta:
        model: ClassVar[type[SupplierCarDiscount]] = SupplierCarDiscount

        fields: ClassVar[list] = [
            'created_at',
            'last_updated',
            'is_active',
            'name',
            'description',
            'precent',
            'start_date',
            'finish_date',
            'supplier',
            'cars',
        ]

        read_only_fields: ClassVar[list] = [
            'created_at',
            'last_updated',
            'is_active',
            'supplier',
        ]

    def validate(self, data: dict) -> dict:
        """
        validate: Validates supplier car discount.

        Args:
            data (dict): Non-validated data.

        Raises:
            serializers.SerializerError: When start date more than finish date.

        Returns:
            dict: Validated data.
        """

        if data['start_date'] >= data['finish_date']:
            raise serializers.ValidationError('Start date must be less than finish date')

        return data


class SupplierCarSerializer(serializers.ModelSerializer):
    """
    SupplierCarSerializer: Serializes supplier car json to py-native types and vice versa.

    Args:
        serializers.ModelSerializer (_type_): Builtin superclass for a SupplierCarSerializer.
    """

    class Meta:
        model: ClassVar[type[SupplierCar]] = SupplierCar

        fields: ClassVar[list] = [
            'created_at',
            'last_updated',
            'is_active',
            'price',
            'supplier',
            'car',
        ]

        read_only_fields: ClassVar[list] = [
            'created_at',
            'last_updated',
            'is_active',
            'price',
            'supplier',
            'car',
        ]


class SupplierHistorySerializer(serializers.ModelSerializer):
    """
    SupplierHistorySerializer: Serializes supplier history json to py-native types and vice versa.

    Args:
        serializers.ModelSerializer (_type_): Builtin superclass for a SupplierHistorySerializer.
    """

    class Meta:
        model: ClassVar[type[SupplierHistory]] = SupplierHistory

        fields: ClassVar[list] = [
            'created_at',
            'last_updated',
            'is_active',
            'supplier',
            'car',
            'sale_price',
            'showroom',
        ]

        read_only_fields: ClassVar[list] = [
            'created_at',
            'last_updated',
            'is_active',
            'supplier',
            'car',
            'sale_price',
            'showroom',
        ]

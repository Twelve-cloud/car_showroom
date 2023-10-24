from typing import ClassVar
from rest_framework import serializers
from customer.models import CustomerModel, CustomerHistory


class CustomerSerializer(serializers.ModelSerializer):
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

    def save(self, **kwargs: dict) -> None:
        customer = super().save(**kwargs)

        if self.instance is None:
            user = kwargs.pop('user')
            customer.user = user

        return customer


class CustomerHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerHistory

        fields = [
            'created_at',
            'last_updated',
            'is_active',
            'customer',
            'car',
            'purchase_price',
            'showroom',
        ]

        read_only_fields = [
            'created_at',
            'last_updated',
            'is_active',
            'customer',
            'car',
            'purchase_price',
            'showroom',
        ]

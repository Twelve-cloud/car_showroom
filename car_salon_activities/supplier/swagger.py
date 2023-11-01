"""
swagger.py: File, containg schema extensions for extend schema decorator.
"""


from rest_framework import status, serializers
from drf_spectacular.utils import OpenApiResponse, inline_serializer
from supplier.serializers import (
    SupplierSerializer,
    SupplierCarSerializer,
    SupplierHistorySerializer,
    SupplierCarDiscountSerializer,
)


supplier_create_schema_extension: dict = {
    'summary': 'New supplier creating',
    'description': """
      Creates new supplier.
    """,
    'request': SupplierSerializer,
    'responses': {
        status.HTTP_201_CREATED: SupplierSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=SupplierSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

supplier_update_schema_extension: dict = {
    'summary': 'Existing supplier updating (all fields)',
    'description': """
      Updates existing supplier (fully).
    """,
    'request': SupplierSerializer,
    'responses': {
        status.HTTP_200_OK: SupplierSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='Unauthorized',
            fields={
                'defail': serializers.CharField(
                    default='Authentication credentials were not provided.',
                ),
            },
        ),
        status.HTTP_403_FORBIDDEN: inline_serializer(
            name='Forbidden',
            fields={
                'detail': serializers.CharField(
                    default='You do not have permission to perform this action.',
                ),
            },
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=SupplierSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

supplier_partial_update_schema_extension: dict = {
    'summary': 'Existing supplier updating (not all fields)',
    'description': """
      Updates existing supplier (partially).
    """,
    'request': SupplierSerializer,
    'responses': {
        status.HTTP_200_OK: SupplierSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='Unauthorized',
            fields={
                'defail': serializers.CharField(
                    default='Authentication credentials were not provided.',
                ),
            },
        ),
        status.HTTP_403_FORBIDDEN: inline_serializer(
            name='Forbidden',
            fields={
                'detail': serializers.CharField(
                    default='You do not have permission to perform this action.',
                ),
            },
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=SupplierSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

supplier_list_schema_extension: dict = {
    'summary': 'Showing all suppliers',
    'description': """
      Shows all suppliers.
    """,
    'responses': {
        status.HTTP_200_OK: SupplierSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='Unauthorized',
            fields={
                'defail': serializers.CharField(
                    default='Authentication credentials were not provided.',
                ),
            },
        ),
        status.HTTP_403_FORBIDDEN: inline_serializer(
            name='Forbidden',
            fields={
                'detail': serializers.CharField(
                    default='You do not have permission to perform this action.',
                ),
            },
        ),
    },
}

supplier_retrieve_schema_extension: dict = {
    'summary': 'Showing concrete supplier',
    'description': """
      Shows information about concrete supplier.
    """,
    'responses': {
        status.HTTP_200_OK: SupplierSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='Unauthorized',
            fields={
                'defail': serializers.CharField(
                    default='Authentication credentials were not provided.',
                ),
            },
        ),
        status.HTTP_403_FORBIDDEN: inline_serializer(
            name='Forbidden',
            fields={
                'detail': serializers.CharField(
                    default='You do not have permission to perform this action.',
                ),
            },
        ),
    },
}

supplier_destroy_schema_extension: dict = {
    'summary': 'Deactivating supplier',
    'description': """
      Deactivates supplier. Marks supplier as inactive insted of deleting it from database.
    """,
    'responses': {
        status.HTTP_204_NO_CONTENT: OpenApiResponse(
            response=None,
            description='Supplier is deactivated.',
        ),
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='Unauthorized',
            fields={
                'defail': serializers.CharField(
                    default='Authentication credentials were not provided.',
                ),
            },
        ),
        status.HTTP_403_FORBIDDEN: inline_serializer(
            name='Forbidden',
            fields={
                'detail': serializers.CharField(
                    default='You do not have permission to perform this action.',
                ),
            },
        ),
    },
}

supplier_make_discount_schema_extension: dict = {
    'summary': 'Making discount for cars of the suppliers.',
    'description': """
      Makes discount for cars of the suppliers.
      When discount is finished then discount will be deleted.
    """,
    'responses': {
        status.HTTP_200_OK: SupplierCarDiscountSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='Unauthorized',
            fields={
                'defail': serializers.CharField(
                    default='Authentication credentials were not provided.',
                ),
            },
        ),
        status.HTTP_403_FORBIDDEN: inline_serializer(
            name='Forbidden',
            fields={
                'detail': serializers.CharField(
                    default='You do not have permission to perform this action.',
                ),
            },
        ),
    },
}

supplier_get_discounts_schema_extension: dict = {
    'summary': 'Gettings discounts for cars of the supplier',
    'description': """
      Returns discounts for cars of the supplier.
    """,
    'responses': {
        status.HTTP_200_OK: SupplierCarDiscountSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='Unauthorized',
            fields={
                'defail': serializers.CharField(
                    default='Authentication credentials were not provided.',
                ),
            },
        ),
        status.HTTP_403_FORBIDDEN: inline_serializer(
            name='Forbidden',
            fields={
                'detail': serializers.CharField(
                    default='You do not have permission to perform this action.',
                ),
            },
        ),
    },
}

supplier_get_statistics_schema_extension: dict = {
    'summary': 'Gettings statistics for supplier',
    'description': """
      Returns statistics for supplier. Includes info about deals with showrooms and suppliers.
    """,
    'responses': {
        status.HTTP_200_OK: SupplierHistorySerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='Unauthorized',
            fields={
                'defail': serializers.CharField(
                    default='Authentication credentials were not provided.',
                ),
            },
        ),
        status.HTTP_403_FORBIDDEN: inline_serializer(
            name='Forbidden',
            fields={
                'detail': serializers.CharField(
                    default='You do not have permission to perform this action.',
                ),
            },
        ),
    },
}

supplier_get_cars_schema_extension: dict = {
    'summary': 'Gettings cars for supplier',
    'description': """
      Returns cars of the supplier.
    """,
    'responses': {
        status.HTTP_200_OK: SupplierCarSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='Unauthorized',
            fields={
                'defail': serializers.CharField(
                    default='Authentication credentials were not provided.',
                ),
            },
        ),
        status.HTTP_403_FORBIDDEN: inline_serializer(
            name='Forbidden',
            fields={
                'detail': serializers.CharField(
                    default='You do not have permission to perform this action.',
                ),
            },
        ),
    },
}

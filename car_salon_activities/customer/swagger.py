"""
swagger.py: File, containg schema extenstions for extend schema decorator.
"""


from rest_framework import status, serializers
from drf_spectacular.utils import OpenApiResponse, inline_serializer
from customer.serializers import CustomerSerializer, CustomerHistorySerializer


customer_create_schema_extenstion: dict = {
    'summary': 'New customer creating',
    'description': """
      Creates new customer and bind user to customer's user field.
    """,
    'request': CustomerSerializer,
    'responses': {
        status.HTTP_201_CREATED: CustomerSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=CustomerSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

customer_update_schema_extension: dict = {
    'summary': 'Existing customer updating (all fields)',
    'description': """
      Updates existing customer (fully).
    """,
    'request': CustomerSerializer,
    'responses': {
        status.HTTP_200_OK: CustomerSerializer,
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
            response=CustomerSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

customer_partial_update_schema_extenstion: dict = {
    'summary': 'Existing customer updating (not all fields)',
    'description': """
      Updates existing customer (partially).
    """,
    'request': CustomerSerializer,
    'responses': {
        status.HTTP_200_OK: CustomerSerializer,
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
            response=CustomerSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

customer_list_schema_extenstion: dict = {
    'summary': 'Showing all customers',
    'description': """
      Shows all customers.
    """,
    'responses': {
        status.HTTP_200_OK: CustomerSerializer,
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

customer_retrieve_schema_extenstion: dict = {
    'summary': 'Showing concrete customer',
    'description': """
      Shows information about concrete customer.
    """,
    'responses': {
        status.HTTP_200_OK: CustomerSerializer,
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

customer_destroy_schema_extenstion: dict = {
    'summary': 'Deactivating customer',
    'description': """
      Deactivates customer. Marks customer as inactive insted of deleting it from database.
    """,
    'responses': {
        status.HTTP_204_NO_CONTENT: OpenApiResponse(
            response=None,
            description='Customer is deactivated.',
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

customer_get_statistics_schema_extension: dict = {
    'summary': 'Gettings statistics for customer',
    'description': """
      Returns statistics for customer. Includes info about deals with showrooms.
    """,
    'responses': {
        status.HTTP_200_OK: CustomerHistorySerializer,
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

customer_make_offer_schema_extensions: dict = {
    'summary': 'Creating customer offer for buying a car.',
    'description': """
      Creates customer offer for buying a car if customer has enough money.
    """,
    'responses': {
        status.HTTP_200_OK: OpenApiResponse(
            response=None,
            description='Offer is created.',
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

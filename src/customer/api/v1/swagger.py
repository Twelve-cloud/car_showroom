"""
swagger.py: File, containg schema extensions for extend schema decorator.
"""


from rest_framework import status
from drf_spectacular.utils import OpenApiResponse
from config.swagger import ForbiddenSerializer, UnauthorizedSerializer
from customer.api.v1.serializers import CustomerSerializer, CustomerHistorySerializer


customer_create_schema_extension: dict = {
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
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=CustomerSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

customer_partial_update_schema_extension: dict = {
    'summary': 'Existing customer updating (not all fields)',
    'description': """
      Updates existing customer (partially).
    """,
    'request': CustomerSerializer,
    'responses': {
        status.HTTP_200_OK: CustomerSerializer,
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=CustomerSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

customer_list_schema_extension: dict = {
    'summary': 'Showing all customers',
    'description': """
      Shows all customers.
    """,
    'responses': {
        status.HTTP_200_OK: CustomerSerializer,
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
    },
}

customer_retrieve_schema_extension: dict = {
    'summary': 'Showing concrete customer',
    'description': """
      Shows information about concrete customer.
    """,
    'responses': {
        status.HTTP_200_OK: CustomerSerializer,
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
    },
}

customer_destroy_schema_extension: dict = {
    'summary': 'Deactivating customer',
    'description': """
      Deactivates customer. Marks customer as inactive insted of deleting it from database.
    """,
    'responses': {
        status.HTTP_204_NO_CONTENT: OpenApiResponse(
            response=None,
            description='Customer is deactivated.',
        ),
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
    },
}

customer_get_statistics_schema_extension: dict = {
    'summary': 'Gettings statistics for customer',
    'description': """
      Returns statistics for customer. Includes info about deals with showrooms.
    """,
    'responses': {
        status.HTTP_200_OK: CustomerHistorySerializer,
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
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
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
    },
}

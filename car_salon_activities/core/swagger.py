"""
swagger.py: File, containg schema extensions for extend schema decorator.
"""


from rest_framework import status, serializers
from drf_spectacular.utils import OpenApiResponse, inline_serializer
from core.serializers import CarSerializer


car_create_schema_extension: dict = {
    'summary': 'New car creating',
    'description': """
      Creates new car.
    """,
    'request': CarSerializer,
    'responses': {
        status.HTTP_201_CREATED: CarSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=CarSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

car_list_schema_extension: dict = {
    'summary': 'Showing all cars',
    'description': """
      Shows all cars.
    """,
    'responses': {
        status.HTTP_200_OK: CarSerializer,
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

car_retrieve_schema_extension: dict = {
    'summary': 'Showing concrete car',
    'description': """
      Shows information about concrete car.
    """,
    'responses': {
        status.HTTP_200_OK: CarSerializer,
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

car_destroy_schema_extension: dict = {
    'summary': 'Deactivating car',
    'description': """
      Deactivates car. Marks car as inactive insted of deleting it from database.
    """,
    'responses': {
        status.HTTP_204_NO_CONTENT: OpenApiResponse(
            response=None,
            description='Car is deactivated.',
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

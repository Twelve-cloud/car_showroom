"""Showroom
swagger.py: File, containg schema extensions for extend schema decorator.
"""


from rest_framework import status
from drf_spectacular.utils import OpenApiResponse
from config.swagger import ForbiddenSerializer, UnauthorizedSerializer
from showroom.serializers import (
    ShowroomSerializer,
    ShowroomCarSerializer,
    ShowroomHistorySerializer,
    ShowroomCarDiscountSerializer,
)


showroom_create_schema_extension: dict = {
    'summary': 'New showroom creating',
    'description': """
      Creates new showroom.
    """,
    'request': ShowroomSerializer,
    'responses': {
        status.HTTP_201_CREATED: ShowroomSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=ShowroomSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

showroom_update_schema_extension: dict = {
    'summary': 'Existing showroom updating (all fields)',
    'description': """
      Updates existing showroom (fully).
    """,
    'request': ShowroomSerializer,
    'responses': {
        status.HTTP_200_OK: ShowroomSerializer,
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=ShowroomSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

showroom_partial_update_schema_extension: dict = {
    'summary': 'Existing showroom updating (not all fields)',
    'description': """
      Updates existing showroom (partially).
    """,
    'request': ShowroomSerializer,
    'responses': {
        status.HTTP_200_OK: ShowroomSerializer,
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=ShowroomSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

showroom_list_schema_extension: dict = {
    'summary': 'Showing all showrooms',
    'description': """
      Shows all showrooms.
    """,
    'responses': {
        status.HTTP_200_OK: ShowroomSerializer,
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
    },
}

showroom_retrieve_schema_extension: dict = {
    'summary': 'Showing concrete showroom',
    'description': """
      Shows information about concrete showroom.
    """,
    'responses': {
        status.HTTP_200_OK: ShowroomSerializer,
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
    },
}

showroom_destroy_schema_extension: dict = {
    'summary': 'Deactivating showroom',
    'description': """
      Deactivates showroom. Marks showroom as inactive insted of deleting it from database.
    """,
    'responses': {
        status.HTTP_204_NO_CONTENT: OpenApiResponse(
            response=None,
            description='Showroom is deactivated.',
        ),
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
    },
}

showroom_make_discount_schema_extension: dict = {
    'summary': 'Making discount for cars of the showrooms.',
    'description': """
      Makes discount for cars of the showrooms.
      When discount is finished then discount will be deleted.
    """,
    'responses': {
        status.HTTP_200_OK: ShowroomCarDiscountSerializer,
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
    },
}

showroom_get_discounts_schema_extension: dict = {
    'summary': 'Gettings discounts for cars of the showroom',
    'description': """
      Returns discounts for cars of the showroom.
    """,
    'responses': {
        status.HTTP_200_OK: ShowroomCarDiscountSerializer,
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
    },
}

showroom_get_statistics_schema_extension: dict = {
    'summary': 'Gettings statistics for showroom',
    'description': """
      Returns statistics for showroom. Includes info about deals with showrooms and suppliers.
    """,
    'responses': {
        status.HTTP_200_OK: ShowroomHistorySerializer,
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
    },
}

showroom_get_cars_schema_extension: dict = {
    'summary': 'Gettings cars for showroom',
    'description': """
      Returns cars of the showroom.
    """,
    'responses': {
        status.HTTP_200_OK: ShowroomCarSerializer,
        status.HTTP_401_UNAUTHORIZED: UnauthorizedSerializer,
        status.HTTP_403_FORBIDDEN: ForbiddenSerializer,
    },
}

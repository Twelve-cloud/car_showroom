"""
swagger.py: File, containg schema extenstions for extend schema decorator.
"""


from rest_framework import status
from drf_spectacular.utils import OpenApiResponse, inline_serializer
from jauth.serializers import UserSerializer, AccessTokenSerializer, RefreshTokenSerializer


user_create_schema_extenstion: dict = {
    'summary': 'New user account creating',
    'description': """
    Creates new User account. After that sends email confirmation link to specified email address.
    Firstly, account will be created as non-active account and non-verified. When email adress is confirmed, account will be activated. # noqa: E501
    If email address is not confirmed for a certain period of time, account will be deleted permanently. # noqa: E501
    """,
    'request': UserSerializer,
    'responses': {
        status.HTTP_201_CREATED: UserSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=UserSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

user_update_schema_extension: dict = {
    'summary': 'Existing user account updating (all fields)',
    'description': """
    Updates existing user account (fully). If email is specified, it also sends email confirmation link to specified email address. # noqa: E501
    Also if email is being updated, then user will be marked as unverified. When email address if confirmed, user account will be verified. # noqa: E501
    """,
    'request': UserSerializer,
    'responses': {
        status.HTTP_200_OK: UserSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='Unauthorized',
            fields={
                'defail': 'Authentication credentials were not provided.',
            },
        ),
        status.HTTP_403_FORBIDDEN: inline_serializer(
            name='Forbidden',
            fields={
                'detail': 'You do not have permission to perform this action.',
            },
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=UserSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

user_partial_update_schema_extenstion: dict = {
    'summary': 'Existing user account updated (not all fields)',
    'description': """
    Updates existing user account (partially). If email is specified, it also sends email confirmation link to specified email address. # noqa: E501
    Also if email is being updated, then user will be marked as unverified. When email address if confirmed, user account will be verified. # noqa: E501
    """,
    'request': UserSerializer,
    'responses': {
        status.HTTP_200_OK: UserSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='Unauthorized',
            fields={
                'defail': 'Authentication credentials were not provided.',
            },
        ),
        status.HTTP_403_FORBIDDEN: inline_serializer(
            name='Forbidden',
            fields={
                'detail': 'You do not have permission to perform this action.',
            },
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=UserSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

user_list_schema_extenstion: dict = {
    'summary': 'Showing all users',
    'description': """
    Shows all users.
    """,
    'responses': {
        status.HTTP_200_OK: UserSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='Unauthorized',
            fields={
                'defail': 'Authentication credentials were not provided.',
            },
        ),
        status.HTTP_403_FORBIDDEN: inline_serializer(
            name='Forbidden',
            fields={
                'detail': 'You do not have permission to perform this action.',
            },
        ),
    },
}

user_retrieve_schema_extenstion: dict = {
    'summary': 'Showing concrete user',
    'description': """
    Shows information about concrete user.
    """,
    'responses': {
        status.HTTP_200_OK: UserSerializer,
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='Unauthorized',
            fields={
                'defail': 'Authentication credentials were not provided.',
            },
        ),
        status.HTTP_403_FORBIDDEN: inline_serializer(
            name='Forbidden',
            fields={
                'detail': 'You do not have permission to perform this action.',
            },
        ),
    },
}

user_destroy_schema_extenstion: dict = {
    'summary': 'Deactivated user account',
    'description': """
    Deactivates user account. Marks user as inactive insted of deleting it from database.
    """,
    'responses': {
        status.HTTP_204_NO_CONTENT: OpenApiResponse(
            response=None,
            description='Account is deactivated.',
        ),
        status.HTTP_401_UNAUTHORIZED: inline_serializer(
            name='Unauthorized',
            fields={
                'defail': 'Authentication credentials were not provided.',
            },
        ),
        status.HTTP_403_FORBIDDEN: inline_serializer(
            name='Forbidden',
            fields={
                'detail': 'You do not have permission to perform this action.',
            },
        ),
    },
}

user_confirm_email_schema_extenstion: dict = {
    'summary': 'Confirming email address of the user',
    'description': """
    Checks confirmation token and if it is OK, then set user as virified. If it is not OK, then send error message. # noqa: E501
    """,
    'responses': {
        status.HTTP_200_OK: OpenApiResponse(
            response=None,
            description='User email address is confirmed.',
        ),
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            name='Token is not correct.',
            fields={
                'Error': 'Bad link.',
            },
        ),
    },
}

user_reset_password_schema_extenstion: dict = {
    'summary': 'Requesting to reset password of the user',
    'description': """
    Requesting to reset password of the user. User email is in urlpath.
    If user is not exist, then sends error message, otherwise sends link to email address.
    """,
    'responses': {
        status.HTTP_200_OK: OpenApiResponse(
            response=None,
            description='Confirmation link has been sent.',
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            response=None,
            description='User with such email is not found.',
        ),
    },
}

user_reset_password_confirm_schema_extenstion: dict = {
    'summary': 'Confirming reset password of the user',
    'description': """
    Confirming password reset. Token is in urlpath. New password is in body.
    If token is correct, then changes user's password otherwise sends error message.
    """,
    'responses': {
        status.HTTP_200_OK: OpenApiResponse(
            response=None,
            description='User has reset its password.',
        ),
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            name='Token is not correct.',
            fields={
                'Error': 'Bad link.',
            },
        ),
    },
}

token_create_schema_extenstion: dict = {
    'summary': 'Creating a pair of token (access and refresh).',
    'description': """
    Creates new pair of token in order to authenticate.
    """,
    'request': AccessTokenSerializer,
    'responses': {
        status.HTTP_201_CREATED: inline_serializer(
            name='Token',
            fields={
                'access': 'token_value',
                'refresh': 'token_value',
            },
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=AccessTokenSerializer,
            description='Fields, that (are not correct)/exists',
        ),
    },
}

token_refresh_schema_extenstion: dict = {
    'summary': 'Refreshing a pair of token.',
    'description': """
    Refreshes expired access token and sends new pair of token.
    """,
    'request': AccessTokenSerializer,
    'responses': {
        status.HTTP_201_CREATED: inline_serializer(
            name='Token',
            fields={
                'access': 'token_value',
                'refresh': 'token_value',
            },
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=RefreshTokenSerializer,
            description='Token is expired/not valid.',
        ),
    },
}

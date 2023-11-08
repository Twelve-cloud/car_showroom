from rest_framework import serializers
from drf_spectacular.utils import inline_serializer


UnauthorizedSerializer = inline_serializer(
    name='Unauthorized',
    fields={
        'defail': serializers.CharField(
            default='Authentication credentials were not provided.',
        ),
    },
)

ForbiddenSerializer = inline_serializer(
    name='Forbidden',
    fields={
        'detail': serializers.CharField(
            default='You do not have permission to perform this action.',
        ),
    },
)

IncorrectTokenSerializer = inline_serializer(
    name='Token is not correct.',
    fields={
        'Error': serializers.CharField(
            default='Bad link.',
        ),
    },
)

TokenPairSerializer = inline_serializer(
    name='Token',
    fields={
        'access': serializers.CharField(
            default='token_value',
        ),
        'refresh': serializers.CharField(
            default='token_value',
        ),
    },
)

from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from jauth.services import get_payload_by_token
from django.shortcuts import get_object_or_404
from jauth.models import User


class JWTMiddleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, request):
        autherization = request.headers.get('Authorization', None)

        if settings.JWT_SCHEME in autherization:
            scheme, access_token = autherization.split()
            payload = get_payload_by_token(access_token)

            if payload is None:
                raise AuthenticationFailed(detail='Unauthorized')

            request.user = get_object_or_404(User, pk=payload.get('sub'))

        response = self.next(request)
        return response

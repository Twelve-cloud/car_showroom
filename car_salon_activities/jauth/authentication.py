from rest_framework import authentication
from django.conf import settings
from jauth.services import get_payload_by_token
from jauth.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            return None

        access_token = self.get_access_token(header)

        if access_token is None:
            return None

        payload = get_payload_by_token(token=access_token)

        if payload is None:
            return None

        user = User.objects.filter(pk=payload.get('sub')).first()

        if user is None:
            return None

        return user, access_token

    def get_header(self, request):
        header = request.META.get(settings.JWT_TOKEN['HEADER_NAME'])
        return header

    def get_access_token(self, header):
        scheme, access_token = header.split()

        if scheme != settings.JWT_TOKEN['TOKEN_TYPE']:
            return None

        return access_token

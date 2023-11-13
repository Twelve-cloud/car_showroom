"""
test_authentication.py: File, containing integration tests for jauth authentication.
"""


import pytest
from rest_framework import status
from jauth.models import User
from jauth.backends import TokenBackend


pytestmark = pytest.mark.django_db


class TestJWTAuth:
    @pytest.fixture(scope='function', autouse=True)
    def admin(self):
        self.admin = User.objects.create(
            username='username1',
            password='password1',
            email='email1@mail.com',
            is_staff=True,
        )

    @pytest.fixture(scope='function', autouse=True)
    def expired_token(self, settings):
        old_access_token_lifetime = settings.JWT_TOKEN['REFRESH_TOKEN_LIFETIME_DAYS']
        settings.JWT_TOKEN['REFRESH_TOKEN_LIFETIME_DAYS'] = 0
        self.expired = TokenBackend.generate_token(type='refresh', user_id=self.admin.id)
        settings.JWT_TOKEN['REFRESH_TOKEN_LIFETIME_DAYS'] = old_access_token_lifetime

    def test_jwt_auth(self, client):
        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_NO_HEADER=f'Bearer {admin_token}')

        response = client.get('/api/v1/supplier/suppliers/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'InvalidTokenType {admin_token}')

        response = client.get('/api/v1/supplier/suppliers/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION='Bearer InvalidToken')

        response = client.get('/api/v1/supplier/suppliers/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        admin_token = TokenBackend.generate_token(type='access', user_id=1000)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get('/api/v1/supplier/suppliers/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.expired}')
        response = client.get('/api/v1/supplier/suppliers/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        client.credentials(HTTP_AUTHORIZATION='InvalidSctructure')
        response = client.get('/api/v1/supplier/suppliers/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get('/api/v1/supplier/suppliers/', format='json')
        assert response.status_code == status.HTTP_200_OK

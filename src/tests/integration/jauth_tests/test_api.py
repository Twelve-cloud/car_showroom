"""
test_api.py: File, containing integration tests for jauth api.
"""


import pytest
from django.conf import settings
from rest_framework import status
from jauth.tasks import send_confirmation_mail
from jauth.models import User
from jauth.backends import TokenBackend


pytestmark = pytest.mark.django_db


class TestUserApi:
    @pytest.fixture(scope='function', autouse=True)
    def no_send_mail(self, mocker):
        mock = mocker.MagicMock()
        mocker.patch.object(send_confirmation_mail, 'delay', mock)

    @pytest.fixture(scope='function', autouse=True)
    def user(self):
        self.user_1 = User.objects.create(
            username='username1',
            password='password1',
            email='email1@mail.com',
        )

        self.user_2 = User.objects.create(
            username='username2',
            password='password2',
            email='email2@mail.com',
        )

    @pytest.fixture(scope='function', autouse=True)
    def user_json(self):
        self.user_json_1 = {
            'username': 'username1',
            'password': 'password1',
            'email': 'email1@mail.com',
        }

        self.user_json_2 = {
            'username': 'username2',
            'password': 'password2',
            'email': 'email2@mail.com',
        }

        self.user_json_3 = {
            'username': 'username3',
            'password': 'password3',
            'email': settings.EMAIL_HOST_USER,
        }

        self.user_json_4 = {
            'username': 'username4',
            'password': 'password4',
            'email': settings.EMAIL_DEF_USER,
        }

        self.u_part_json = {
            'username': 'partial_username',
        }

    def test_create_user(self, client):
        response = client.post('/api/v1/auth/users/', self.user_json_3, format='json')
        user = User.objects.filter(username=self.user_json_3.get('username')).first()
        assert user is not None
        assert response.status_code == status.HTTP_201_CREATED

        response = client.post('/api/v1/auth/users/', self.user_json_3, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        user_token = TokenBackend.generate_token(type='access', user_id=user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.post('/api/v1/auth/users/', self.user_json_3, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        user.is_staff = True
        user.save(update_fields=['is_staff'])
        response = client.post('/api/v1/auth/users/', self.user_json_4, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_user(self, client):
        response = client.put(
            f'/api/v1/auth/users/{self.user_1.id}/',
            self.user_json_3,
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user_1.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.put(
            f'/api/v1/auth/users/{self.user_1.id}/',
            self.user_json_3,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

        response = client.put(
            f'/api/v1/auth/users/{self.user_2.id}/',
            self.user_json_4,
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = client.put(
            f'/api/v1/auth/users/{self.user_1.id}/',
            self.u_part_json,
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = client.put(
            f'/api/v1/auth/users/{self.user_1.id}/',
            self.user_json_2,
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_partial_update_user(self, client):
        response = client.patch(
            f'/api/v1/auth/users/{self.user_1.id}/',
            self.user_json_3,
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user_1.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.patch(
            f'/api/v1/auth/users/{self.user_1.id}/',
            self.user_json_3,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

        response = client.patch(
            f'/api/v1/auth/users/{self.user_2.id}/',
            self.user_json_4,
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = client.patch(
            f'/api/v1/auth/users/{self.user_1.id}/',
            self.u_part_json,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

        response = client.patch(
            f'/api/v1/auth/users/{self.user_1.id}/',
            self.user_json_2,
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_users(self, client):
        response = client.get('/api/v1/auth/users/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user_1.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get('/api/v1/auth/users/', format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_user(self, client):
        response = client.get(f'/api/v1/auth/users/{self.user_1.id}/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user_1.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get(f'/api/v1/auth/users/{self.user_1.id}/', format='json')
        assert response.status_code == status.HTTP_200_OK

        response = client.get(f'/api/v1/auth/users/{self.user_2.id}/', format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_destroy_user(self, client):
        response = client.delete(f'/api/v1/auth/users/{self.user_1.id}/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user_1.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.delete(f'/api/v1/auth/users/{self.user_2.id}/', format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = client.delete(f'/api/v1/auth/users/{self.user_1.id}/', format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT

        self.user_1.is_staff = True
        self.user_1.save(update_fields=['is_staff'])
        response = client.delete(f'/api/v1/auth/users/{self.user_2.id}/', format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_confirm_email(self, client):
        user_token = TokenBackend.generate_token(type='access', user_id=self.user_1.id)

        response = client.get(f'/api/v1/auth/users/confirm_email/{user_token}/', format='json')
        assert response.status_code == status.HTTP_200_OK

        response = client.get('/api/v1/auth/users/confirm_email/bad_token/', format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get(f'/api/v1/auth/users/confirm_email/{user_token}/', format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_reset_password(self, client):
        request_body = {'email': self.user_1.email}
        response = client.post('/api/v1/auth/users/reset_password/', request_body, format='json')
        assert response.status_code == status.HTTP_200_OK

        request_body = {'email': 'invalid_email'}
        response = client.post('/api/v1/auth/users/reset_password/', request_body, format='json')
        assert response.status_code == status.HTTP_404_NOT_FOUND

        user_token = TokenBackend.generate_token(type='access', user_id=self.user_1.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.post('/api/v1/auth/users/reset_password/', request_body, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_reset_password_confirm(self, client):
        user_token = TokenBackend.generate_token(type='access', user_id=self.user_1.id)
        request_body = {'password': '12341234'}

        response = client.patch(
            f'/api/v1/auth/users/reset_password_confirm/{user_token}/',
            request_body,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

        response = client.patch(
            '/api/v1/auth/users/reset_password_confirm/bad_token/',
            request_body,
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.patch(
            f'/api/v1/auth/users/reset_password_confirm/{user_token}/',
            request_body,
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestTokenApi:
    @pytest.fixture(scope='function', autouse=True)
    def user(self):
        self.verified_user = User.objects.create(
            username='username1',
            password='password1',
            email='email1@mail.com',
            is_verified=True,
        )

        self.verified_user.set_password(self.verified_user.password)

        self.unverified_user = User.objects.create(
            username='username2',
            password='password2',
            email='email2@mail.com',
        )

        self.unverified_user.set_password(self.unverified_user.password)

    @pytest.fixture(scope='function', autouse=True)
    def credentials(self):
        self.credentials = {
            'email': 'email1@mail.com',
            'password': 'password1',
        }

        self.invalid_password = {
            'email': 'email1@mail.com',
            'password': 'password',
        }

        self.invalid_creds = {
            'email': 'invalid_email',
            'password': 'invalid_password',
        }

        self.unverified_creds = {
            'email': 'email2@mail.com',
            'password': 'password2',
        }

    @pytest.fixture(scope='function')
    def expired_token(self, settings):
        old_access_token_lifetime = settings.JWT_TOKEN['REFRESH_TOKEN_LIFETIME_DAYS']
        settings.JWT_TOKEN['REFRESH_TOKEN_LIFETIME_DAYS'] = 0
        self.expired = TokenBackend.generate_token(type='refresh', user_id=self.verified_user.id)
        settings.JWT_TOKEN['REFRESH_TOKEN_LIFETIME_DAYS'] = old_access_token_lifetime

    def test_create_token(self, client):
        response = client.post('/api/v1/auth/token/', self.invalid_creds, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = client.post('/api/v1/auth/token/', self.invalid_password, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = client.post('/api/v1/auth/token/', self.unverified_creds, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = client.post('/api/v1/auth/token/', self.credentials, format='json')
        assert response.status_code == status.HTTP_200_OK

        self.verified_user.is_active = True
        self.verified_user.save(update_fields=['is_active'])

        response = client.post('/api/v1/auth/token/', self.credentials, format='json')
        assert response.status_code == status.HTTP_200_OK

        user_token = TokenBackend.generate_token(type='access', user_id=self.verified_user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.post('/api/v1/auth/token/', self.credentials, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_refresh_token(self, client, expired_token):
        response = client.post(
            '/api/v1/auth/token/refresh/',
            {'refresh': 'invalid' * 10},
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = client.post(
            '/api/v1/auth/token/refresh/',
            {'refresh': self.expired},
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        refresh = {
            'refresh': TokenBackend.generate_token(type='refresh', user_id=1000),
        }

        response = client.post('/api/v1/auth/token/refresh/', refresh, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        refresh = {
            'refresh': TokenBackend.generate_token(type='refresh', user_id=self.verified_user.id),
        }

        response = client.post('/api/v1/auth/token/refresh/', refresh, format='json')
        assert response.status_code == status.HTTP_200_OK

        user_token = TokenBackend.generate_token(type='access', user_id=self.verified_user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.post('/api/v1/auth/token/refresh/', refresh, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

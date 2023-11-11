"""
test_api.py: File, containing integration tests for core api.
"""


import pytest
from rest_framework import status
from core.models import CarModel
from jauth.models import User
from jauth.backends import TokenBackend


pytestmark = pytest.mark.django_db


class TestCarApi:
    @pytest.fixture(scope='function', autouse=True)
    def admin(self):
        self.admin = User.objects.create(
            username='username1',
            password='password1',
            email='email1@mail.com',
            is_staff=True,
        )

    @pytest.fixture(scope='function', autouse=True)
    def user(self):
        self.user = User.objects.create(
            username='username2',
            password='password2',
            email='email2@mail.com',
        )

    @pytest.fixture(scope='function', autouse=True)
    def car(self):
        self.car = CarModel.objects.create(
            brand='tesla',
            transmission_type='auto',
            creation_year=2000,
            miliage=200000.0,
        )

    @pytest.fixture(scope='function', autouse=True)
    def car_json(self):
        self.car_json = {
            'brand': 'audi',
            'transmission_type': 'auto',
            'creation_year': 2000,
            'miliage': 200000.0,
        }

    def test_create_car(self, client):
        response = client.post('/api/v1/core/cars/', self.car_json, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.post('/api/v1/core/cars/', self.car_json, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.post('/api/v1/core/cars/', self.car_json, format='json')
        assert CarModel.objects.filter(**self.car_json).exists() is True
        assert response.status_code == status.HTTP_201_CREATED

    def test_list_cars(self, client):
        response = client.get('/api/v1/core/cars/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get('/api/v1/core/cars/', format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get('/api/v1/core/cars/', format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_car(self, client):
        response = client.get(f'/api/v1/core/cars/{self.car.id}/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get(f'/api/v1/core/cars/{self.car.id}/', format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get(f'/api/v1/core/cars/{self.car.id}/', format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_destroy_car(self, client):
        response = client.delete(f'/api/v1/core/cars/{self.car.id}/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.delete(f'/api/v1/core/cars/{self.car.id}/', format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.delete(f'/api/v1/core/cars/{self.car.id}/', format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT

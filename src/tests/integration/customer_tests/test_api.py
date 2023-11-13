"""
test_api.py: File, containing integration tests for customer api.
"""


import pytest
from rest_framework import status
from core.tasks import make_customer_offer
from core.models import CarModel
from jauth.models import User
from jauth.backends import TokenBackend
from customer.models import CustomerModel


pytestmark = pytest.mark.django_db


class TestCustomerApi:
    @pytest.fixture(scope='function', autouse=True)
    def no_make_offer(self, mocker):
        mock = mocker.MagicMock()
        mocker.patch.object(make_customer_offer, 'delay', mock)

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
    def customer(self):
        self.customer = CustomerModel.objects.create(
            balance=3000.0,
            user=User.objects.create(
                username='customer_user',
                password='customer_password',
                email='customer_email@mail.com',
            ),
        )

    @pytest.fixture(scope='function', autouse=True)
    def customer_json(self):
        self.customer_json = {
            'balance': 10000.0,
        }

    @pytest.fixture(scope='function', autouse=True)
    def offer_json(self):
        self.offer_json = {
            'customer': self.customer.id,
            'max_price': 2000.0,
            'car': CarModel.objects.create(
                brand='audi',
                transmission_type='auto',
                creation_year=2000,
                miliage=2000.00,
            ).id,
        }

    def test_create_customer(self, client):
        response = client.post('/api/v1/customer/customers/', self.customer_json, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.post('/api/v1/customer/customers/', self.customer_json, format='json')
        assert CustomerModel.objects.filter(user=self.user).exists() is True
        assert response.status_code == status.HTTP_201_CREATED

        response = client.post('/api/v1/customer/customers/', self.customer_json, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.post('/api/v1/customer/customers/', {}, format='json')
        assert CustomerModel.objects.filter(user=self.admin).exists() is True
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_customer(self, client):
        response = client.put(
            f'/api/v1/customer/customers/{self.customer.id}/',
            self.customer_json,
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.put(
            f'/api/v1/customer/customers/{self.customer.id}/',
            self.customer_json,
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.put(
            f'/api/v1/customer/customers/{self.customer.id}/',
            self.customer_json,
            format='json',
        )
        assert CustomerModel.objects.filter(**self.customer_json).exists() is True
        assert response.status_code == status.HTTP_200_OK

    def test_partial_update_customer(self, client):
        response = client.patch(
            f'/api/v1/customer/customers/{self.customer.id}/',
            self.customer_json,
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.patch(
            f'/api/v1/customer/customers/{self.customer.id}/',
            self.customer_json,
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.patch(
            f'/api/v1/customer/customers/{self.customer.id}/',
            self.customer_json,
            format='json',
        )
        assert CustomerModel.objects.filter(**self.customer_json).exists() is True
        assert response.status_code == status.HTTP_200_OK

    def test_list_customers(self, client):
        response = client.get('/api/v1/customer/customers/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get('/api/v1/customer/customers/', format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get('/api/v1/customer/customers/', format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_customer(self, client):
        response = client.get(f'/api/v1/customer/customers/{self.customer.id}/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get(f'/api/v1/customer/customers/{self.customer.id}/', format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get(f'/api/v1/customer/customers/{self.customer.id}/', format='json')
        assert response.status_code == status.HTTP_200_OK

        customer_token = TokenBackend.generate_token(type='access', user_id=self.customer.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {customer_token}')

        response = client.get(f'/api/v1/customer/customers/{self.customer.id}/', format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_destroy_customer(self, client):
        response = client.delete(f'/api/v1/customer/customers/{self.customer.id}/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.delete(f'/api/v1/customer/customers/{self.customer.id}/', format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.delete(f'/api/v1/customer/customers/{self.customer.id}/', format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_get_customer_statistics(self, client):
        response = client.get(
            f'/api/v1/customer/customers/{self.customer.id}/get_statistics/',
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get(
            f'/api/v1/customer/customers/{self.customer.id}/get_statistics/',
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get(
            f'/api/v1/customer/customers/{self.customer.id}/get_statistics/',
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

        customer_token = TokenBackend.generate_token(type='access', user_id=self.customer.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {customer_token}')

        response = client.get(
            f'/api/v1/customer/customers/{self.customer.id}/get_statistics/',
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

    def test_make_customer_offer(self, client):
        response = client.post(
            f'/api/v1/customer/customers/{self.customer.id}/make_offer/',
            self.offer_json,
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.post(
            f'/api/v1/customer/customers/{self.customer.id}/make_offer/',
            self.offer_json,
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.post(
            f'/api/v1/customer/customers/{self.customer.id}/make_offer/',
            self.offer_json,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

        customer_token = TokenBackend.generate_token(type='access', user_id=self.customer.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {customer_token}')

        response = client.post(
            f'/api/v1/customer/customers/{self.customer.id}/make_offer/',
            self.offer_json,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

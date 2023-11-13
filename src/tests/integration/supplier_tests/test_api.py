"""
test_api.py: File, containing integration tests for supplier api.
"""


from datetime import datetime, timedelta
import pytest
from rest_framework import status
from core.models import CarModel
from jauth.models import User
from jauth.backends import TokenBackend
from supplier.models import SupplierCar, SupplierModel, SupplierHistory, SupplierCarDiscount


pytestmark = pytest.mark.django_db


class TestSupplierApi:
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
            brand='audi',
            transmission_type='auto',
            creation_year=2000,
            miliage=2000.00,
        )

    @pytest.fixture(scope='function', autouse=True)
    def supplier(self):
        self.supplier = SupplierModel.objects.create(
            name='supplier1',
            creation_year=2001,
            customers_count=21,
            number_of_sales=21,
            discount_for_unique_customers=0.5,
        )

        SupplierCar.objects.create(
            price=1000,
            car=self.car,
            supplier=self.supplier,
        )

        SupplierCarDiscount.objects.create(
            name='discount',
            description='description',
            precent=0.3,
            start_date=datetime.now(),
            finish_date=datetime.now() + timedelta(hours=1),
            supplier=self.supplier,
        ).cars.set([self.car])

        SupplierHistory.objects.create(
            supplier=self.supplier,
            car=self.car,
            sale_price=5000.00,
        )

    @pytest.fixture(scope='function', autouse=True)
    def supplier_json(self):
        self.supplier_json = {
            'name': 'supplier',
            'creation_year': 2000,
            'customers_count': 20,
            'number_of_sales': 20,
            'discount_for_unique_customers': 0.3,
        }

    @pytest.fixture(scope='function', autouse=True)
    def discount_json(self):
        self.discount_json = {
            'name': 'discount',
            'description': 'description',
            'precent': 0.3,
            'start_date': datetime.now(),
            'finish_date': datetime.now() + timedelta(hours=1),
            'supplier': SupplierModel.objects.create(
                name='supplier2',
                creation_year=2002,
                customers_count=22,
                number_of_sales=22,
                discount_for_unique_customers=0.2,
            ).id,
            'cars': [
                self.car.id,
            ],
        }

    @pytest.fixture(scope='function', autouse=True)
    def invalid_discount_json(self):
        self.invalid_discount_json = {
            'name': 'discount',
            'description': 'description',
            'precent': 0.3,
            'start_date': datetime.now() + timedelta(hours=1),
            'finish_date': datetime.now(),
            'supplier': SupplierModel.objects.create(
                name='supplier3',
                creation_year=2003,
                customers_count=23,
                number_of_sales=23,
                discount_for_unique_customers=0.3,
            ).id,
            'cars': [
                self.car.id,
            ],
        }

    def test_create_supplier(self, client):
        response = client.post('/api/v1/supplier/suppliers/', self.supplier_json, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.post('/api/v1/supplier/suppliers/', self.supplier_json, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.post('/api/v1/supplier/suppliers/', self.supplier_json, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_supplier(self, client):
        response = client.put(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/',
            self.supplier_json,
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.put(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/',
            self.supplier_json,
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.put(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/',
            self.supplier_json,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

    def test_partial_update_supplier(self, client):
        response = client.patch(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/',
            self.supplier_json,
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.patch(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/',
            self.supplier_json,
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.patch(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/',
            self.supplier_json,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

    def test_list_suppliers(self, client):
        response = client.get('/api/v1/supplier/suppliers/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get('/api/v1/supplier/suppliers/', format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get('/api/v1/supplier/suppliers/', format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_supplier(self, client):
        response = client.get(f'/api/v1/supplier/suppliers/{self.supplier.id}/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get(f'/api/v1/supplier/suppliers/{self.supplier.id}/', format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get(f'/api/v1/supplier/suppliers/{self.supplier.id}/', format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_destroy_supplier(self, client):
        response = client.delete(f'/api/v1/supplier/suppliers/{self.supplier.id}/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.delete(f'/api/v1/supplier/suppliers/{self.supplier.id}/', format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.delete(f'/api/v1/supplier/suppliers/{self.supplier.id}/', format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_make_supplier_discount(self, client):
        response = client.post(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/make_discount/',
            self.discount_json,
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.post(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/make_discount/',
            self.discount_json,
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.post(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/make_discount/',
            self.discount_json,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

        response = client.post(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/make_discount/',
            self.invalid_discount_json,
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_supplier_discounts(self, client):
        response = client.get(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/get_discounts/',
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/get_discounts/',
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/get_discounts/',
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_supplier_statistics(self, client):
        response = client.get(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/get_statistics/',
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/get_statistics/',
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/get_statistics/',
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_supplier_cars(self, client):
        response = client.get(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/get_cars/',
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/get_cars/',
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get(
            f'/api/v1/supplier/suppliers/{self.supplier.id}/get_cars/',
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

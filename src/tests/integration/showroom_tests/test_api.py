"""
test_api.py: File, containing integration tests for showroom api.
"""


from datetime import datetime, timedelta
import pytest
from rest_framework import status
from django_countries.fields import Country
from core.models import CarModel
from jauth.models import User
from jauth.backends import TokenBackend
from showroom.models import ShowroomCar, ShowroomModel, ShowroomHistory, ShowroomCarDiscount


pytestmark = pytest.mark.django_db


class TestShowroomApi:
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
    def showroom(self):
        self.showroom = ShowroomModel.objects.create(
            name='showroom1',
            creation_year=2001,
            balance=0.0,
            location=Country(code='NZ'),
            charts={},
            number_of_sales=20,
            discount_for_unique_customers=0.3,
        )

        ShowroomCar.objects.create(
            price=1000,
            car=self.car,
            showroom=self.showroom,
        )

        ShowroomCarDiscount.objects.create(
            name='discount',
            description='description',
            precent=0.3,
            start_date=datetime.now(),
            finish_date=datetime.now() + timedelta(hours=1),
            showroom=self.showroom,
        ).cars.set([self.car])

        ShowroomHistory.objects.create(
            showroom=self.showroom,
            car=self.car,
            sale_price=5000.00,
        )

    @pytest.fixture(scope='function', autouse=True)
    def showroom_json(self):
        self.showroom_json = {
            'name': 'showroom',
            'creation_year': 2000,
            'balance': 0.0,
            'location': 'NZ',
            'charts': [
                {
                    'brand': 'audi',
                    'transmission_type': 'auto',
                    'creation_year': '2000',
                    'miliage': '2000.00',
                },
            ],
            'number_of_sales': 20,
            'discount_for_unique_customers': 0.3,
        }

    @pytest.fixture(scope='function', autouse=True)
    def partial_showroom_json(self):
        self.partial_showroom_json = {
            'name': 'showroom',
            'creation_year': 2000,
            'balance': 0.0,
            'location': 'NZ',
            'number_of_sales': 20,
            'discount_for_unique_customers': 0.3,
        }

    @pytest.fixture(scope='function', autouse=True)
    def invalid_showroom_json(self):
        self.inv_showroom_json = {
            'name': 'showroom',
            'creation_year': 2000,
            'balance': 0.0,
            'location': 'NZ',
            'charts': {'invalid': 'charts'},
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
            'showroom': ShowroomModel.objects.create(
                name='showroom2',
                creation_year=2002,
                balance=0.0,
                location=Country(code='NZ'),
                charts={},
                number_of_sales=20,
                discount_for_unique_customers=0.3,
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
            'showroom': ShowroomModel.objects.create(
                name='showroom3',
                creation_year=2003,
                balance=0.0,
                location=Country(code='NZ'),
                charts={},
                number_of_sales=20,
                discount_for_unique_customers=0.3,
            ).id,
            'cars': [
                self.car.id,
            ],
        }

    def test_create_showroom(self, client):
        response = client.post('/api/v1/showroom/showrooms/', self.showroom_json, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.post('/api/v1/showroom/showrooms/', self.showroom_json, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.post('/api/v1/showroom/showrooms/', self.inv_showroom_json, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        response = client.post('/api/v1/showroom/showrooms/', self.showroom_json, format='json')
        assert response.status_code == status.HTTP_201_CREATED

        showroom = ShowroomModel.objects.get(name=self.showroom_json['name'])
        assert self.car in showroom.appropriate_cars.all()

    def test_update_showroom(self, client):
        response = client.put(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/',
            self.showroom_json,
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.put(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/',
            self.showroom_json,
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.put(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/',
            self.showroom_json,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

    def test_partial_update_showroom(self, client):
        response = client.patch(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/',
            self.partial_showroom_json,
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.patch(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/',
            self.partial_showroom_json,
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.patch(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/',
            self.partial_showroom_json,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

    def test_list_showrooms(self, client):
        response = client.get('/api/v1/showroom/showrooms/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get('/api/v1/showroom/showrooms/', format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get('/api/v1/showroom/showrooms/', format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_showroom(self, client):
        response = client.get(f'/api/v1/showroom/showrooms/{self.showroom.id}/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get(f'/api/v1/showroom/showrooms/{self.showroom.id}/', format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get(f'/api/v1/showroom/showrooms/{self.showroom.id}/', format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_destroy_showroom(self, client):
        response = client.delete(f'/api/v1/showroom/showrooms/{self.showroom.id}/', format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.delete(f'/api/v1/showroom/showrooms/{self.showroom.id}/', format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.delete(f'/api/v1/showroom/showrooms/{self.showroom.id}/', format='json')
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_make_showroom_discount(self, client):
        response = client.post(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/make_discount/',
            self.discount_json,
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.post(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/make_discount/',
            self.discount_json,
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.post(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/make_discount/',
            self.discount_json,
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

        response = client.post(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/make_discount/',
            self.invalid_discount_json,
            format='json',
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_showroom_discounts(self, client):
        response = client.get(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/get_discounts/',
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/get_discounts/',
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/get_discounts/',
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_showroom_statistics(self, client):
        response = client.get(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/get_statistics/',
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/get_statistics/',
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/get_statistics/',
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

    def test_get_showroom_cars(self, client):
        response = client.get(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/get_cars/',
            format='json',
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        user_token = TokenBackend.generate_token(type='access', user_id=self.user.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token}')

        response = client.get(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/get_cars/',
            format='json',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        admin_token = TokenBackend.generate_token(type='access', user_id=self.admin.id)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token}')

        response = client.get(
            f'/api/v1/showroom/showrooms/{self.showroom.id}/get_cars/',
            format='json',
        )
        assert response.status_code == status.HTTP_200_OK

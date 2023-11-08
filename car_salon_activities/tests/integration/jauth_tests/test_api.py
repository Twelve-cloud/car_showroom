import pytest
from rest_framework import status


pytestmark = pytest.mark.django_db


class TestJauthApi:
    @pytest.fixture(scope='function', autouse=True)
    def user_json(self):
        self.user_json = {
            'username': 'username1',
            'password': 'password1',
            'email': 'email@mail.com',
        }

    def test_create_user(self, client):
        response = client.post('/auth/users/', self.user_json, format='json')

        assert response.status_code == status.HTTP_201_CREATED

from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from reggit import apiviews

class TestPost(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.uri = '/posts/'
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()


    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )


    def test_list(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200,
            'Expected Response Code 200, received {0} instead.'
            .format(response.status_code))
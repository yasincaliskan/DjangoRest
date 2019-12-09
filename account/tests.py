from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.utils import json


class UserRegistrationTestCase(APITestCase):
    url = reverse("account:register")
    url_login = reverse("token_obtain_pair")

    #Register operation for correct data
    def test_user_registration(self):
        data = {
            "username" : "yaskotest",
            "password" : "a123a123"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    #Invalid password
    def test_user_invalid_password(self):
        data = {
            "username" : "yaskotest",
            "password" : "1"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    #Unique username
    def test_unique_name(self):
        self.test_user_registration()
        data = {
            "username" : "yaskotest",
            "password" : "a123a123a123"
        }

        response = self.client.post(self.url, data)
        self.assertEqual(400, response.status_code)

    #User don't see page register with session
    def test_user_authenticated_registration(self):
        self.test_user_registration()
        self.client.login(username = 'yaskotest', password = 'a123a123')
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

    # User don't see page register with token
    def test_user_authenticated_token_registration(self):
        self.test_user_registration()
        data = {
            "username": "yaskotest",
            "password": "a123a123"
        }
        response = self.client.post(self.url_login, data)
        self.assertEqual(200, response.status_code)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer ' + token)
        response2 = self.client.get(self.url)
        self.assertEqual(403, response2.status_code)

class UserLogin(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "yaskotest"
        self.password = "a123a123"
        self.user = User.objects.create_user(username = self.username, password=self.password)

    def test_user_token(self):
        response = self.client.post(self.url_login, {'username': 'yaskotest', 'password': 'a123a123'})
        self.assertEqual(200, response.status_code)
        self.assertTrue('access' in json.loads(response.content))

    def test_user_invalid_data(self):
        response = self.client.post(self.url_login, {'username': 'invalid', 'password': 'askdajslda'})
        self.assertEqual(401, response.status_code)

    def test_user_empty_data(self):
        response = self.client.post(self.url_login, {'username': '', 'password': ''})
        self.assertEqual(400, response.status_code)

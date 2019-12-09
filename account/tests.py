from rest_framework.test import APITestCase
from django.urls import reverse

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


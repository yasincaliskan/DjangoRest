from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.utils import json
from post.models import Post


class FavouriteCreateList(APITestCase):
    url_create = reverse("post:create")
    url_list = reverse("post:list")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "yaskotest"
        self.password = "test1234"
        self.user = User.objects.create_user(username = self.username, password = self.password)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.url_login, data = {'username': self.username, 'password': self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_add_new_post(self):
        data = {
            'content': 'xxx',
            'title': 'header'
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(201, response.status_code)

    def test_add_new_post_unauthorization(self):
        self.client.credentials()

        data = {
            'content': 'xxx',
            'title': 'header'
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(403, response.status_code)

    #Post list
    def test_posts(self):
        self.test_add_new_post()
        response = self.client.get(self.url_list)
        self.assertTrue(len(json.loads(response.content)["results"]) == Post.objects.all().count())


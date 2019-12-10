from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.utils import json

from favourite.models import Favourite
from post.models import Post


class FavouriteCreateList(APITestCase):
    url = reverse("favourite:list-create")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "yaskotest"
        self.password = "test1234"
        self.post = Post.objects.create(title="Header", content="Content-xxx")
        self.user = User.objects.create_user(username = self.username, password = self.password)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.url_login, data = {'username': self.username, 'password': self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    #Add favourite
    def test_add_favourite(self):
        data = {
            "content": "Nice Content",
            "user": self.user.id,
            "post": self.post.id
        }

        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_user_favs(self):
        self.test_add_favourite()
        response = self.client.get(self.url)
        self.assertTrue(len(json.loads(response.content)["results"]) == Favourite.objects.filter(user = self.user).count())

class FavouriteUpdateDelete(APITestCase):
    login_url = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "yaskotest"
        self.password = "test1234"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="test2", password=self.password)
        self.post = Post.objects.create(title="Header", content="Content-xxx")
        self.favourite = Favourite.objects.create(content="xxx-Content", post =self.post, user = self.user)
        self.url = reverse("favourite:update-delete", kwargs={"pk":self.favourite.pk})
        self.test_jwt_authentication()

    def test_jwt_authentication(self, username = "yaskotest", password = "test1234"):
        response = self.client.post(self.login_url, data = {'username': username, 'password': password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    #Destroy Favourite
    def test_fav_delete(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)

    #Destroy fav different user
    def test_fav_delete_different_user(self):
        self.test_jwt_authentication("test2")
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)

    #Update favourite
    def test_fav_update(self):
        data = {
            "content": "any content"
        }

        response = self.client.put(self.url, data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(Favourite.objects.get(id = self.favourite.id).content == data["content"])

    #Any user processing different user favourite content
    def test_fav_update_different_user(self):
        self.test_jwt_authentication("yaskotest")
        data = {
            "content": "wrong content!",
            "user": self.user2.id,
        }

        response = self.client.put(self.url)
        self.assertTrue(403, response.status_code)

    #Unauthorazation
    def test_unauthorazation(self):
        self.client.credentials() #Log out
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

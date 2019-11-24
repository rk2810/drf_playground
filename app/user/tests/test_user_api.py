from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test the public user APIs"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """test valid user creation payload"""
        payload = {
            "email": "test1@email.com",
            "name": "rohan test",
            "password": "testpass",
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_duplicate(self):
        """test to create a user that already exists"""
        payload = {
            "email": "test1@email.com",
            "name": "rohan test",
            "password": "testpass",
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_strong(self):
        """password must be stroncc"""
        payload = {"email": "test1@email.com", "name": "rohan test", "password": "test"}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()

        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test if token is created for user"""
        payload = {"email": "test1@test.com", "password": "testpass"}
        user = create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    def test_token_for_invalid_user_credentials(self):
        """check that token doesnt come up if user credentials are wrong."""
        user = create_user(email="test1@test.com", password="testpass")
        payload = {"email": "test1@test.com", "password": "wrongpass"}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_for_user_not_exists(self):
        """test that token is not generated if user does not exists."""
        payload = {"email": "test1@test.com", "password": "wrongpass"}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_for_missing_fields(self):
        """test that token is not generated if fields are missing."""
        payload = {"email": "test1@test.com", "password": ""}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

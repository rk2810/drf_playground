from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    return get_user_model().objects.create(**params)


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

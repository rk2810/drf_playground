from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer


RECIPE_URL = reverse("recipe:recipe-list")


def sample_recipe(user, **params):
    """create and return a sample recipe"""
    defaults = {"title": "Sample Recipe", "time_minutes": 10, "price": 5.00}
    defaults.update(params)

    return Recipe.objects.create(user=user, **defaults)


class PublicRecipeTestAPI(TestCase):
    """publicly available recipe api for unauth'd user"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """test aun auth'd request"""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeTestAPI(TestCase):
    """private API for recipes for authenticated user"""

    def setUp(self):
        self.client = APIClient()

        self.user_payload = {"email": "test@test.com", "password": "testpass"}

        self.user = get_user_model().objects.create_user(**self.user_payload)
        self.client.force_authenticate(self.user)

    def test_retrieve_list_recipes(self):
        """test the  list of created recipes of a user"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by("-id")

        serializer = RecipeSerializer(recipes, many=True)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """test that only recipes of a user show up"""

        user2 = get_user_model().objects.create_user(
            email="user2@test.com", password="password2"
        )

        sample_recipe(user=user2)
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

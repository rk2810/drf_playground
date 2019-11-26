from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient


from core.models import Ingredient, Recipe

from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse("recipe:ingredient-list")


class PublicIngredientAPITest(TestCase):
    """Test publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITest(TestCase):
    """Test private ingredient API"""

    def setUp(self):
        payload = {"email": "test@test.com", "password": "testpass"}
        self.user = get_user_model().objects.create_user(**payload)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """test retrieval of ingredients"""
        Ingredient.objects.create(user=self.user, name="Chilly")
        Ingredient.objects.create(user=self.user, name="Cucumber")

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        payload = {"email": "test1@test.com", "password": "testpass"}
        user2 = get_user_model().objects.create_user(**payload)
        Ingredient.objects.create(user=user2, name="Kale")
        ingredient = Ingredient.objects.create(user=self.user, name="Salt")

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)

    def test_create_ingredient_successful(self):
        payload = {"name": "Test Ingredient"}
        self.client.post(INGREDIENT_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user, name=payload["name"]
        ).exists()

        self.assertTrue(exists)

    def test_create_invalid_ingredient(self):
        payload = {"name": ""}

        res = self.client.post(INGREDIENT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_assigned_ingredients(self):
        """retrieve the ingredients that are assigned to recipe"""
        ing1 = Ingredient.objects.create(user=self.user, name="Chicken")
        ing2 = Ingredient.objects.create(user=self.user, name="Cucumber")

        recipe = Recipe.objects.create(
            **{
                "title": "Chicken Tikka",
                "time_minutes": 30,
                "price": 10.00,
                "user": self.user,
            }
        )

        recipe.ingredients.add(ing1)

        res = self.client.get(INGREDIENT_URL, {"assigned_only": 1})

        serializer1 = IngredientSerializer(ing1)
        serializer2 = IngredientSerializer(ing2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_get_unique_distinct_ingredients(self):
        """retrieve only distinct ingredients from filtering"""
        ing = Ingredient.objects.create(user=self.user, name="Chicken")
        Ingredient.objects.create(user=self.user, name="Cucumber")

        recipe1 = Recipe.objects.create(
            **{
                "title": "Chicken Tikka",
                "time_minutes": 10,
                "price": 10.00,
                "user": self.user,
            }
        )
        recipe1.ingredients.add(ing)

        recipe2 = Recipe.objects.create(
            **{
                "title": "Chicken Curry",
                "time_minutes": 10,
                "price": 10.00,
                "user": self.user,
            }
        )

        recipe2.ingredients.add(ing)

        res = self.client.get(INGREDIENT_URL, {"assigned_only": 1})

        self.assertEqual(len(res.data), 1)

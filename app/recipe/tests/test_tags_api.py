from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient


from core.models import Tag, Recipe

from recipe.serializers import TagSerializer


TAGS_URL = reverse("recipe:tag-list")


class PublicTagsAPITest(TestCase):
    """Test publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsAPITest(TestCase):
    """Test private tags API"""

    def setUp(self):
        payload = {"email": "test@test.com", "password": "testpass"}
        self.user = get_user_model().objects.create_user(**payload)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """test retrieval of tags"""
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Dessert")

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        payload = {"email": "test1@test.com", "password": "testpass"}
        user2 = get_user_model().objects.create_user(**payload)
        Tag.objects.create(user=user2, name="Fruity")
        tag = Tag.objects.create(user=self.user, name="Healthy")

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], tag.name)

    def test_create_tag_successful(self):
        payload = {"name": "Test tag"}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(user=self.user, name=payload["name"]).exists()

        self.assertTrue(exists)

    def test_create_invalid_tag(self):
        payload = {"name": ""}

        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_assigned_tags(self):
        """retrieve the tags that are assigned to recipe"""
        tag1 = Tag.objects.create(user=self.user, name="Breakfast")
        tag2 = Tag.objects.create(user=self.user, name="Lunch")

        recipe = Recipe.objects.create(
            **{
                "title": "Eggs and toast",
                "time_minutes": 10,
                "price": 5.00,
                "user": self.user,
            }
        )

        recipe.tags.add(tag1)

        res = self.client.get(TAGS_URL, {"assigned_only": 1})

        serializer1 = TagSerializer(tag1)
        serializer2 = TagSerializer(tag2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_get_unique_distinct_tags(self):
        """retrieve only distinct tags from filtering"""
        tag = Tag.objects.create(user=self.user, name="Breakfast")
        Tag.objects.create(user=self.user, name="Lunch")

        recipe1 = Recipe.objects.create(
            **{"title": "Pancake", "time_minutes": 10, "price": 3.00, "user": self.user}
        )
        recipe1.tags.add(tag)

        recipe2 = Recipe.objects.create(
            **{"title": "Porridge", "time_minutes": 5, "price": 2.00, "user": self.user}
        )

        recipe2.tags.add(tag)

        res = self.client.get(TAGS_URL, {"assigned_only": 1})

        self.assertEqual(len(res.data), 1)

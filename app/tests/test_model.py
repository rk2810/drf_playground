from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


User = get_user_model()


def sample_user(email="test@test.com", password="testpass"):
    return get_user_model().objects.create_user(email, password)


class UserModelTest(TestCase):
    """Test case for the User model"""

    def test_create_user_with_email(self):
        """Create new user with email """
        email = "test@test.com"
        password = "testpass"
        user = User.objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_email_is_normalized(self):
        email = "teSt@TEST.cOm"
        password = "test"
        user = User.objects.create_user(email, password)
        self.assertEqual(user.email, email.lower())

    def test_create_new_superuser(self):
        """Test for creating a superuser"""
        user = User.objects.create_superuser("superuser@test.com", "1234")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """ Test string representation of tag"""
        tag = models.Tag.objects.create(user=sample_user(), name="Vegan",)

        self.assertEqual(str(tag), tag.name)

    def test_ingridient_str(self):
        ingredient = models.Ingredient.objects.create(
            user=sample_user(), name="Cucumber",
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """check recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(), title="New Recipe", time_minutes=5, price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch("uuid.uuid4")
    def test_recipe_filename_uuid(self, mock_uuid):
        """Test image is saved correctly"""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, "image.jpg")

        expected_path = f"uploads/recipe/{uuid}.jpg"
        self.assertEqual(file_path, expected_path)

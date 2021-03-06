import uuid
import os

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings


def recipe_image_file_path(instance, filename):
    """generate filepath for recipe image"""
    extension = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"

    return os.path.join("uploads/recipe/", filename)


class UserManager(BaseUserManager):
    """Custom user manager"""

    def normalize_email2(self, email):
        """since normalize_email only checks the domain so lower the whole email altogether was a good idea."""
        email = self.normalize_email(email).lower()
        return email

    def create_user(self, email, password=None, **extra_fields):
        """Create and save user"""
        user = self.model(email=self.normalize_email2(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model to support email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Tag(models.Model):
    """A tag for a recipe"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """An ingredient for a recipe"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe oject"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title

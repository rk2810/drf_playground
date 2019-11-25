from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Tag, Ingredient, Recipe

from recipe.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeDetailSerializer,
    RecipeImageSerializer,
)


class BaseRecipeAttr(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    """Base class for recipe attributes like tags and ingredients"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """return QS for current user only"""
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """ create a new object"""
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttr):
    """Manage tags in DB"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseRecipeAttr):
    """Manage tags in DB"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in DB"""

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """return QS for current user only"""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """get serializer based on request"""
        if self.action == "retrieve":
            return RecipeDetailSerializer
        elif self.action == "upload_image":
            return RecipeImageSerializer

        return RecipeSerializer

    def perform_create(self, serializer):
        """create a new recipe object"""
        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Upload image to recipe"""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

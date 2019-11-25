from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe


class TagSerializer(serializers.ModelSerializer):
    """serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ("id", "name")
        read_only_fields = ("id",)


class IngredientSerializer(serializers.ModelSerializer):
    """serializer for tag objects"""

    class Meta:
        model = Ingredient
        fields = ("id", "name")
        read_only_fields = ("id",)


class RecipeSerializer(serializers.ModelSerializer):
    """serializer for recipe object"""

    ingredients = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ("id", "title", "ingredients", "price", "time_minutes", "tags", "link")
        read_only_fields = ("id",)


class RecipeDetailSerializer(RecipeSerializer):
    """Serialize a single recipe for details"""

    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True)


class RecipeImageSerializer(serializers.ModelSerializer):
    """Upload image serializer for recipes"""

    class Meta:
        model = Recipe
        fields = ("id", "image")
        read_only_fields = ("id",)

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import SmallRecipeSerializer, UsersSerializer

from .models import (Favorite, Ingredients, Recipe, RecipeIngredients,
                     ShoppingCart, Tags)

RECIPES_ERROR_MESSAGES = {
    'cooking_time_not_positive':
        'Время приготовления не может быть отрицательным или нулём.',
    'cooking_time_too_big':
        'Время приготовления слишком большое.',
    'ingredients_is_none':
        'Вы не добавили ингердиенты.',
    'ingredients_not_unique':
        'Вы добавили одинаковые ингердиенты, удалите их.',
    'ingredients_amount_not_positive':
        'Количество ингредиента не может быть отрицательным или нулём.',
    'ingredients_amount_too_big':
        'Количество ингредиента слишком большое.'
}


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Ingredients


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        read_only=True,
        source='ingredients.id'
    )
    name = serializers.CharField(
        read_only=True,
        source='ingredients.name',
    )
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredients.measurement_unit'
    )

    class Meta:
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )
        model = RecipeIngredients


class RecipeIngredientsCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(write_only=True)
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        model = RecipeIngredients
        fields = (
            'id',
            'amount'
        )


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Tags


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(
        read_only=True,
        many=True
    )
    author = UsersSerializer(
        read_only=True
    )
    ingredients = RecipeIngredientsSerializer(
        read_only=True,
        source='recipeingredients_set',
        many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        exclude = ('pub_date', )
        model = Recipe

    def get_is_favorited(self, instance):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favorite.objects.filter(
                favorite_user=user,
                favorite_recipe=instance
            ).exists()
        return False

    def get_is_in_shopping_cart(self, instance):
        user = self.context['request'].user
        if user.is_authenticated:
            return ShoppingCart.objects.filter(
                shopping_cart_user=user,
                shopping_cart_recipe=instance
            ).exists()
        return False


class CreateOrUpdateRecipeSerializer(serializers.ModelSerializer):
    author = UsersSerializer(read_only=True)
    ingredients = RecipeIngredientsCreateSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField()

    class Meta:
        fields = ('__all__')
        model = Recipe

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        cooking_time = self.initial_data.get('cooking_time')
        if int(cooking_time) <= 0:
            raise serializers.ValidationError(
                RECIPES_ERROR_MESSAGES['cooking_time_not_positive']
            )
        if int(cooking_time) > 1140:
            raise serializers.ValidationError(
                RECIPES_ERROR_MESSAGES['cooking_time_too_big']
            )
        if len(ingredients) == 0:
            raise serializers.ValidationError(
                RECIPES_ERROR_MESSAGES['ingredients_is_none']
            )
        if len(ingredients) != len(list(
                {
                    ing['id']: ing
                    for ing in ingredients
                }.values())):
            raise serializers.ValidationError(
                RECIPES_ERROR_MESSAGES['ingredients_not_unique']
            )
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise serializers.ValidationError(
                    RECIPES_ERROR_MESSAGES['ingredients_amount_not_positive']
                )
            if int(ingredient['amount']) > 9999:
                raise serializers.ValidationError(
                    RECIPES_ERROR_MESSAGES['ingredients_amount_too_big']
                )
        return data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        author = self.context['request'].user
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.save()
        recipe.tags.set(tags_data)
        recipe_ingredients = [
            RecipeIngredients(
                recipe=recipe,
                ingredients=Ingredients.objects.get(id=ingredient['id']),
                amount=ingredient['amount']
            )
            for ingredient in ingredients_data
        ]
        RecipeIngredients.objects.bulk_create(recipe_ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        instance.author = self.context['request'].user
        instance.name = validated_data.pop('name')
        instance.text = validated_data.pop('text')
        instance.cooking_time = validated_data.pop('cooking_time')
        if validated_data.get('image') is not None:
            instance.image = validated_data.pop('image')
        instance.save()
        instance.tags.set(tags_data)
        RecipeIngredients.objects.filter(recipe=instance).delete()
        recipe_ingredients = [
            RecipeIngredients(
                recipe=instance,
                ingredients=Ingredients.objects.get(id=ingredient['id']),
                amount=ingredient['amount']
            )
            for ingredient in ingredients_data
        ]
        RecipeIngredients.objects.bulk_create(recipe_ingredients)
        return instance

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context=self.context
        )
        return serializer.data


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Favorite
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['favorite_user', 'favorite_recipe']
            )
        ]

    def to_representation(self, instance):
        serializer = SmallRecipeSerializer(
            instance.favorite_recipe,
            context=self.context
        )
        return serializer.data


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = ShoppingCart
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['shopping_cart_user', 'shopping_cart_recipe']
            )
        ]

    def to_representation(self, instance):
        serializer = SmallRecipeSerializer(
            instance.shopping_cart_recipe,
            context=self.context
        )
        return serializer.data

import base64
from rest_framework import serializers
import ast
from django.core.files.base import ContentFile
import webcolors
from users.serializers import UsersSerializer
from .models import Recipe, Ingredients, RecipeIngredients, Tags


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        try:
            value = webcolors.hex_to_name(value)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredients


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        read_only=True,
        source='ingredients.name'
    )
    measurement_unit = serializers.CharField(
        read_only=True,
        source='ingredients.measurement_unit'
    )

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = RecipeIngredients


class TagsSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        fields = '__all__'
        model = Tags


class RecipeSerializer(serializers.ModelSerializer):
    author = UsersSerializer()
    tags = TagsSerializer(
        many=True
    )
    ingredients = RecipeIngredientsSerializer(
        source='recipeingredients_set',
        many=True
    )

    class Meta:
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time',
        )
        model = Recipe


class RecipeCreateOrUpdateSerializer(serializers.ModelSerializer):

    author = UsersSerializer(
        read_only=True
    )

    class Meta:
        fields = (
            'id', 'ingredients', 'tags', 'author', 'image',
            'name', 'text', 'cooking_time',
        )
        model = Recipe

    def to_internal_value(self, data):
        tags_data = data.get('tags')
        ingredients_data = data.get('ingredients')
        image = data.get('image')
        ingredients = ast.literal_eval(ingredients_data)
        tags = [
            int(tag) for tag in tags_data.split(',')
        ]
        if isinstance(image, str) and image.startswith('data:image'):
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]
            image = ContentFile(
                base64.b64decode(imgstr), name='recipes.' + ext
            )
        return {
            'tags': tags,
            'ingredients': ingredients,
            'image': image,
            'name': data.get('name'),
            'text': data.get('text'),
            'cooking_time': data.get('cooking_time'),
        }

    def to_representation(self, value):
        if isinstance(value, Recipe):
            serializer = RecipeSerializer(value)
        else:
            raise Exception
        return serializer.data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        author = self.context['request'].user
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.save()
        recipe.tags.set(tags_data)
        for ingredient in ingredients_data:
            recipe_ingredient = Ingredients.objects.get(id=ingredient['id'])
            amount = ingredient['amount']
            RecipeIngredients.objects.create(
                recipe=recipe, ingredients=recipe_ingredient, amount=amount
            )
        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        instance.author = self.context['request'].user
        instance.image = validated_data.get(
            'image', instance.image
        )
        instance.name = validated_data.get(
            'name', instance.name
        )
        instance.text = validated_data.get(
            'text', instance.text
        )
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.save()
        instance.tags.set(tags_data)
        RecipeIngredients.objects.filter(recipe=instance).delete()
        for ingredient in ingredients_data:
            recipe_ingredient = Ingredients.objects.get(id=ingredient['id'])
            amount = ingredient['amount']
            RecipeIngredients.objects.update_or_create(
                recipe=instance, ingredients=recipe_ingredient, amount=amount
            )
        return instance

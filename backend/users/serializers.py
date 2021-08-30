from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe
from users.models import CustomUser, Follow


class UsersSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }
        model = CustomUser

    def get_is_subscribed(self, instance):
        user = self.context['request'].user
        if user.is_authenticated:
            return Follow.objects.filter(
                user=user,
                author=instance
            ).exists()
        return False


class SmallRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        model = Recipe


class RecipeAuthorSerializer(UsersSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        model = CustomUser

    def get_recipes(self, instance):
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit'
        )
        recipes = Recipe.objects.filter(
            author=instance
        )
        if recipes_limit:
            serializer = SmallRecipeSerializer(
                recipes[:int(recipes_limit)],
                many=True
            )
            return serializer.data
        serializer = SmallRecipeSerializer(
            recipes,
            many=True
        )
        return serializer.data

    def get_recipes_count(self, instanse):
        recipes_count = Recipe.objects.filter(author=instanse).count()
        return recipes_count


class SubscriptionsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'author']
            )
        ]

    def validate(self, data):
        if self.context['request'].user != data.get('author'):
            return data
        raise serializers.ValidationError(
            'Вы не можете подписаться на самого себя!'
        )

    def to_representation(self, instance):
        if isinstance(instance, Follow):
            serializer = RecipeAuthorSerializer(
                instance.author,
                context=self.context
            )
        else:
            raise Exception
        return serializer.data

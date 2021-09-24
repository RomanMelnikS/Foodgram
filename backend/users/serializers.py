from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import CustomUser, Subscription

USERS_ERROR_MESSAGES = {
    'subscribe_to_yourself': 'Вы не можете подписаться на самого себя!'
}


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
            return Subscription.objects.filter(
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
        model = Subscription
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['user', 'author']
            )
        ]

    def validate(self, data):
        if self.context['request'].user != data.get('author'):
            return data
        raise serializers.ValidationError(
            USERS_ERROR_MESSAGES['subscribe_to_yourself']
        )

    def to_representation(self, instance):
        serializer = RecipeAuthorSerializer(
            instance.author,
            context=self.context
        )
        return serializer.data

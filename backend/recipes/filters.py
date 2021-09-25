import django_filters as filters

from users.models import CustomUser

from .models import Ingredients, Recipe, Tags


class RecipesFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tags.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        field_name='favorite_recipe',
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='shopping_cart_recipe',
        method='get_is_in_shopping_cart'
    )
    author = filters.ModelChoiceFilter(queryset=CustomUser.objects.all())

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value:
                return queryset.filter(
                    favorite_recipe__favorite_user=self.request.user
                )
            return queryset.exclude(
                favorite_recipe__favorite_user=self.request.user
            )
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated:
            if value:
                return queryset.filter(
                    shopping_cart_recipe__shopping_cart_user=self.request.user
                )
            return queryset.exclude(
                shopping_cart_recipe__shopping_cart_user=self.request.user
            )
        return queryset

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
            'author'
        )


class IngredientsFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        fields = (
            'name',
        )
        model = Ingredients

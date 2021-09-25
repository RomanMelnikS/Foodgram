from django.contrib import admin
from django.utils.html import format_html

from api_foodgram.settings import DEFAULT_EMPTY_VALUE_DISPLAY

from .models import (Favorite, Ingredients, Recipe, RecipeIngredients,
                     ShoppingCart, Tags)


class RecipeIndredientsAdmin(admin.TabularInline):
    list_display = (
        'ingredients',
        'amount'
    )
    model = RecipeIngredients


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    def count_favorite_recipes(self, obj):
        return Favorite.objects.filter(favorite_recipe=obj).count()
    count_favorite_recipes.short_description = 'Число добавлений в избранное'

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{0}" style="max-width: 50%"/>',
                obj.image.url
            )
    image_tag.short_description = 'Превью'

    readonly_fields = (
        'count_favorite_recipes',
        'image_tag'
    )

    fields = (
        'tags',
        'author',
        'name',
        'image',
        'image_tag',
        'text',
        'cooking_time',
        'count_favorite_recipes'
    )

    list_display = (
        'name',
        'author'
    )
    list_filter = (
        'author',
        'name',
        'tags'
    )
    empty_value_display = DEFAULT_EMPTY_VALUE_DISPLAY
    inlines = [
        RecipeIndredientsAdmin,
    ]


@admin.register(Ingredients)
class IndredientsAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    list_filter = (
        'name',
    )


@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug'
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'favorite_user',
        'favorite_recipe'
    )


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'shopping_cart_user',
        'shopping_cart_recipe'
    )

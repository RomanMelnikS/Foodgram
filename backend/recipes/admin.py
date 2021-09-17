from django.contrib import admin
from django.utils.html import format_html
from recipes.models import (Favorite, Ingredients, Recipe, RecipeIngredients,
                            ShoppingCart, Tags)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'text',
        'author',
        'image_tag',
        'image',
        'cooking_time'
    )
    readonly_fields = ('image_tag',)
    search_fields = ('ingredients',)
    empty_value_display = '-пусто-'

    def image_tag(self, recipe):
        if recipe.image:
            return format_html(
                '<img src="{0}" style="max-width: 100%"/>',
                recipe.image.url
            )
    image_tag.short_description = 'Превью'


@admin.register(Ingredients)
class IndredientsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit'
    )


@admin.register(RecipeIngredients)
class RecipeIndredientsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipe',
        'ingredients',
        'amount'
    )


@admin.register(Tags)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
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

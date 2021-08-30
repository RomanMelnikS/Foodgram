from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор рецепта',
        null=False
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        null=False
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка',
        blank=True,
        null=False
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        null=False
    )
    ingredients = models.ManyToManyField(
        'Ingredients',
        through='RecipeIngredients',
        related_name='ingredients',
        verbose_name='Ингредиенты',
        blank=True
    )
    tags = models.ManyToManyField(
        'Tags',
        related_name='tags',
        verbose_name='Тэг',
        blank=True
    )
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, 'Не меньше 1 мин'),
        ],
        verbose_name='Время приготовления',
        null=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return (self.name)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Ingredients(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        null=False
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        null=False
    )

    def __str__(self):
        return (self.name)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    ingredients = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )

    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, 'Не меньше 1 ед'),
        ],
        verbose_name='Количество ингредиентов',
        null=True
    )

    def __str__(self):
        return (self.ingredients.name)

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Tags(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тэга',
        null=False
    )
    color = models.TextField(
        max_length=200,
        verbose_name='Цвет тэга',
        default='#5662f6',
        null=False
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Slug',
        unique=True,
        null=False
    )

    def __str__(self):
        return (self.name)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Favorite(models.Model):
    favorite_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь',
        null=True
    )
    favorite_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Рецепт',
        null=True
    )

    def __str__(self):
        return ('Избранное')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(models.Model):
    shopping_cart_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart_user',
        verbose_name='Пользователь',
        null=True
    )
    shopping_cart_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipe',
        verbose_name='Рецепт',
        null=True
    )

    def __str__(self):
        return ('Список покупок')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

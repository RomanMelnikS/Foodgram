from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

import webcolors
from users.models import CustomUser


class Recipe(models.Model):
    tags = models.ManyToManyField(
        'Tags',
        related_name='tags',
        verbose_name='Тэг',
        blank=True
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Автор рецепта',
        null=False
    )
    ingredients = models.ManyToManyField(
        'Ingredients',
        through='RecipeIngredients',
        related_name='ingredients',
        verbose_name='Ингредиенты',
        blank=True
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
    cooking_time = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, 'Не меньше 1'),
            MaxValueValidator(999, 'Не больше 999')
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

    MEASUREMENT_UNITS = [
        ('г', 'грамм'),
        ('стакан', 'стакан'),
        ('по вкусу', 'по вкусу'),
        ('ст. л.', 'столовая ложка'),
        ('шт.', 'штук'),
        ('мл', 'миллилитр'),
        ('ч. л.', 'чайная ложка'),
        ('капля', 'капля'),
        ('звездочка', 'звездочка'),
        ('щепотка', 'щепотка'),
        ('горсть', 'горсть'),
        ('кусок', 'кусок'),
        ('кг', 'килограмм'),
        ('пакет', 'пакет'),
        ('пучок', 'пучок'),
        ('долька', 'долька'),
        ('банка', 'банка'),
        ('упаковка', 'упаковка'),
        ('зубчик', 'зубчик'),
        ('пласт', 'пласт'),
        ('пачка', 'пачка'),
        ('тушка', 'тушка'),
        ('стручок', 'стручок'),
        ('веточка', 'веточка'),
        ('бутылка', 'бутылка'),
        ('л', 'литр'),
        ('батон', 'батон'),
        ('пакетик', 'пакетик'),
        ('лист', 'лист'),
        ('стебель', 'стебель')
    ]

    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
        null=False
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        choices=MEASUREMENT_UNITS,
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
            MinValueValidator(1, 'Не меньше 1'),
            MaxValueValidator(9999, 'Не больше 9999')
        ],
        verbose_name='Количество ингредиентов',
        null=False
    )

    def __str__(self):
        return (self.ingredients.name)

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Tags(models.Model):

    HEX_COLORS = [
        ('#00ffff', 'aqua'),
        ('#000000', 'black'),
        ('#0000ff', 'blue'),
        ('#ff00ff', 'fuchsia'),
        ('#008000', 'green'),
        ('#808080', 'gray'),
        ('#00ff00', 'lime'),
        ('#800000', 'maroon'),
        ('#000080', 'navy'),
        ('#808000', 'olive'),
        ('#800080', 'purple'),
        ('#ff0000', 'red'),
        ('#c0c0c0', 'silver'),
        ('#008080', 'teal'),
        ('#ffffff', 'white'),
        ('#ffff00', 'yellow'),
        ('#ff1493', 'deeppink'),
        ('#deb887', 'burlywood'),
        ('#b8860b', 'darkgoldenrod'),
        ('#4b0082', 'indigo')
    ]

    def valdate_color(self, value):
        match = webcolors.HEX_COLOR_RE.match(value)
        if match is None:
            raise ValidationError(
                f'{value} недопустимое шестнадцатеричное значение цвета.',
                params={'value': value},
            )
        return match

    name = models.CharField(
        max_length=200,
        verbose_name='Название тэга',
        null=False
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет тэга в HEX',
        choices=HEX_COLORS,
        validators=[valdate_color],
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

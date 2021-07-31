from django.db import models
from django.core.validators import MinValueValidator
from users.models import CustomUser


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
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
        verbose_name='Ингредиенты',
        blank=True
    )
    tag = models.ManyToManyField(
        'Tag',
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

    def __str__(self):
        return (self.name)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Ingredients(models.Model):

    class Ingredient(models.Choices):
        (
            ('title', 'title'),
        )

    title = models.CharField(
        choices=Ingredient.choices,
        max_length=200,
        verbose_name='Название ингредиента',
        null=False
    )
    quantity = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, 'Не меньше 1 ед'),
        ],
        verbose_name='Количество ингредиентов',
        null=True
    )
    dimension = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        null=False
    )

    def __str__(self):
        return (self.title)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Tag(models.Model):
    name = models.TextField(
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


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Follower'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Following',
        null=True
    )

    def __str__(self):
        return ('Подписки')

    class Meta:
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь',
        null=True
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранное',
        null=True
    )

    def __str__(self):
        return ('Избранное')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

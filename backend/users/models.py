from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Имя под которым вы будете отображаться на сайте',
        null=False
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Фамилия под которой вы будете отображаться на сайте',
        null=False
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Электронная почта',
        help_text='Адрес вашей эл.почты',
        unique=True
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # def set_password(self, password):
    #     return super().set_password(password)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


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

from django.db import models
import textwrap as tw

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        GUEST = 'guest', 'guest'
        AUTH_USER = 'auth_user', 'auth_user'
        ADMIN = 'admin', 'admin'

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
    role = models.CharField(
        choices=Role.choices,
        max_length=50,
        verbose_name='Роль пользователя',
        default=Role.GUEST
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def set_password(self, password):
        return super().set_password(password)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return tw.shorten(self.email, width=15, placeholder='...')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

from django.contrib import admin

from users.models import CustomUser, Follow


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'first_name',
        'last_name',
        'username',
        'email',
        'password'
    )
    empty_value_display = '-пусто-'
    model = CustomUser


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )

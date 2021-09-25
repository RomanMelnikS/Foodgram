from django.contrib import admin

from api_foodgram.settings import DEFAULT_EMPTY_VALUE_DISPLAY

from .models import CustomUser, Subscription


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
    list_filter = (
        'email',
        'username'
    )
    empty_value_display = DEFAULT_EMPTY_VALUE_DISPLAY
    model = CustomUser


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )

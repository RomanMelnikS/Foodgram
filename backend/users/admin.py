from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api_foodgram.settings import DEFAULT_EMPTY_VALUE_DISPLAY
from .models import CustomUser, Subscription


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
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

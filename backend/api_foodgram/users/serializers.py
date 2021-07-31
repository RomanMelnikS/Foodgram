from rest_framework import serializers

from .models import CustomUser


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        # filter_backends = (filters.SearchFilter, filters.OrderingFilter)
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }
        model = CustomUser

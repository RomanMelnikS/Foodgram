from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.views import CustomPageNumberPagination

from .models import CustomUser, Subscription
from .serializers import SubscriptionsSerializer


class UsersViewSet(UserViewSet):
    pagination_class = CustomPageNumberPagination

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated],
        name='subscriptions',
        url_name='subscriptions',
        url_path='subscriptions'
    )
    def subscriptions(self, request):
        user = self.request.user
        subscriptions = Subscription.objects.filter(user=user)
        page = self.paginate_queryset(subscriptions)
        serializer = SubscriptionsSerializer(
            page,
            many=True,
            context={
                'request': request
            }
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['get', 'delete'],
        permission_classes=[IsAuthenticated],
        name='subscribe',
        url_name='subscribe',
        url_path='subscribe'
    )
    def subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(
            CustomUser,
            id=id
        )
        if request.method == 'GET':
            serializer = SubscriptionsSerializer(
                data={
                    'user': user.id,
                    'author': author.id
                },
                context={
                    'request': request
                }
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription = get_object_or_404(
            Subscription,
            user=user,
            author=author
        )
        subscription.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

from django.shortcuts import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from recipes.filters import RecipesFilter, IngredientsFilter
from recipes.permissions import IsAuthor
from recipes.models import (Favorite, Ingredients, Recipe, RecipeIngredients,
                            ShoppingCart, Tags)
from recipes.serializers import (CreateOrUpdateRecipeSerializer,
                                 FavoriteSerializer, IngredientsSerializer,
                                 RecipeSerializer, ShoppingCartSerializer,
                                 TagsSerializer)


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 150


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    lookup_field = 'id'
    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAuthor],
        'delete': [IsAuthor],
        'favorite': [IsAuthenticated],
        'add_to_shopping_cart': [IsAuthenticated],
        'download_shopping_cart': [IsAuthenticated],

    }
    pagination_class = CustomPageNumberPagination
    filterset_class = RecipesFilter
    filterset_fields = ['tags', 'is_favorite', 'is_in_shopping_cart']
    ordering = ('-pub_date',)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return CreateOrUpdateRecipeSerializer
        return RecipeSerializer

    def get_permissions(self):
        return [
            permission() for permission
            in self.permission_classes_by_action[self.action]
        ]

    @action(
        detail=True,
        methods=['get', 'delete'],
        name='favorite',
        url_name='favorite',
        url_path='favorite'
    )
    def favorite(self, request, id=None):
        user = self.request.user
        recipe = get_object_or_404(
            Recipe,
            id=id
        )
        if request.method == 'GET':
            serializer = FavoriteSerializer(
                data={
                    'favorite_user': user.id,
                    'favorite_recipe': recipe.id
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
        favorite_recipe = get_object_or_404(
            Favorite,
            favorite_user=user,
            favorite_recipe=recipe
        )
        favorite_recipe.delete()
        return Response(
            'Recipe deleted from favorites.',
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=True,
        methods=['get', 'delete'],
        name='add_to_shopping_cart',
        url_name='shopping_cart',
        url_path='shopping_cart'
    )
    def add_to_shopping_cart(self, request, id=None):
        user = self.request.user
        recipe = get_object_or_404(
            Recipe,
            id=id
        )
        if request.method == 'GET':
            serializer = ShoppingCartSerializer(
                data={
                    'shopping_cart_user': user.id,
                    'shopping_cart_recipe': recipe.id
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
        shopping_cart_recipe = get_object_or_404(
            ShoppingCart,
            shopping_cart_user=user,
            shopping_cart_recipe=recipe
        )
        shopping_cart_recipe.delete()
        return Response(
            'Recipe deleted from shopping cart.',
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        detail=False,
        methods=['get'],
        name='download_shopping_cart',
        url_name='download_shopping_cart',
        url_path='download_shopping_cart'
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        shopping_cart_recipes = ShoppingCart.objects.filter(
            shopping_cart_user=user
        )
        shopping_cart = {}
        for recipe in shopping_cart_recipes:
            for ingredient in recipe.shopping_cart_recipe.ingredients.all():
                ing = RecipeIngredients.objects.get(
                    ingredients=ingredient,
                    recipe=recipe.shopping_cart_recipe
                )
                total_amount = ing.amount
                if ingredient.name not in shopping_cart:
                    shopping_cart[ingredient.name] = (
                        str(total_amount), ingredient.measurement_unit
                    )
                else:
                    total_amount += ing.amount
                    shopping_cart[ingredient.name] = (
                        str(total_amount), ingredient.measurement_unit
                    )
        shop_list = ';\n'.join(
            [
                ' - '.join(
                    (ing, shopping_cart[ing][0] + shopping_cart[ing][1])
                )
                for ing in shopping_cart
            ]
        )
        content = (
            f'{user.username},\nВот необходимые для приготовления ингредиенты:\
                \n{shop_list}.\nСходи и купи!!!'
        )
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(
            'shopping_cart_list.txt')
        return response


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()
    lookup_field = 'id'
    filterset_class = IngredientsFilter
    filterset_fields = ['name', ]
    ordering = ('id',)
    pagination_class = None


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    lookup_field = 'id'
    ordering = ('id',)
    pagination_class = None

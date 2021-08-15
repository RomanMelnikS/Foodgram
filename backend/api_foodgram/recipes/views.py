from rest_framework import filters, viewsets
from .models import Ingredients, Recipe, Tags
from .serializers import (
    RecipeSerializer, IngredientsSerializer, TagsSerializer,
    RecipeCreateOrUpdateSerializer
)
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    lookup_field = 'id'
    queryset = Recipe.objects.all()
    search_fields = ('name',)
    ordering = ('id',)
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return RecipeCreateOrUpdateSerializer
        return RecipeSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientsSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    lookup_field = 'id'
    queryset = Ingredients.objects.all()
    search_fields = ('name',)
    ordering = ('id',)


class TagsViewSet(viewsets.ModelViewSet):
    serializer_class = TagsSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    lookup_field = 'id'
    queryset = Tags.objects.all()
    search_fields = ('name',)
    ordering = ('id',)

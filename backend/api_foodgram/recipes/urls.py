from .views import RecipeViewSet, IngredientsViewSet, TagsViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls))
]

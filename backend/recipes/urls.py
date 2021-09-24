from django.urls import include, path
from recipes.views import IngredientsViewSet, RecipeViewSet, TagsViewSet
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()

router_v1.register(
    r'recipes',
    RecipeViewSet,
    basename='recipes'
)
router_v1.register(
    r'ingredients',
    IngredientsViewSet,
    basename='ingredients'
)
router_v1.register(
    r'tags',
    TagsViewSet,
    basename='tags'
)

urlpatterns = [
    path('', include(router_v1.urls))
]

from django.urls import path, include
from api.views import (
    UserViewSet,
    AuthTokenView,
    AuthTokenLogoutView,
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet)
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('auth/token/login/', AuthTokenView.as_view()),
    path('auth/token/logout/', AuthTokenLogoutView.as_view()),
    path('', include(router.urls)),
]

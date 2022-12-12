from django.urls import path, include
from api.views import UserViewSet, AuthTokenView
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('auth/token/login/', AuthTokenView.as_view()),
    path('', include(router.urls)),
]

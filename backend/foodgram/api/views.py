from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from djoser.views import TokenCreateView

from recipes.models import User
from api.serializers import UserSerializer, PasswordSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet для доступа к пользователям."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_value_regex = '[^/.]+'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        if (
            self.queryset.filter(email=email).exists()
            or self.queryset.filter(username=username).exists()
        ):
            return Response(
                {'Такой email существует.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = self.get_serializer(
            user, data=request.data, partial=True
        )
        if serializer.is_valid():
            if not user.is_admin and 'role' in serializer.validated_data:
                serializer.validated_data.pop('role')
            serializer.save(**serializer.validated_data)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[permissions.IsAuthenticated],
    )
    def set_password(self, request):
        user = get_object_or_404(User, username=request.user)
        serializer = PasswordSerializer(
            user, data=request.data, partial=True
        )
        if serializer.is_valid():
            password = serializer.validated_data.pop('new_password')
            _ = serializer.validated_data.pop('current_password')
            serializer.save(password=password, **serializer.validated_data)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AuthTokenView(TokenCreateView):
    """View класс для получения токена."""
    permission_classes = [permissions.AllowAny]

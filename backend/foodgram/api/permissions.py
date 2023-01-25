from rest_framework import permissions


class IsAdminOrOwnerOrReadOnly(permissions.BasePermission):
    """
    Полное разрешение для Администратора и Владельца,
    только чтение для остальных.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin or (
                obj.author == request.user
            )
        )


class IsAuthenticatedForDetail(permissions.BasePermission):
    """
    Разрешение на доступ к объектам для аутентифицированных
    пользователей.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated

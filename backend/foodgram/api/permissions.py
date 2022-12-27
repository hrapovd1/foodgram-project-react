from rest_framework import permissions


class IsAdminOrOwnerOrReadOnly(permissions.BasePermission):
    """
    Полное разрешение для Администратора и Владельца,
    только чтение для остальных.
    """
    def has_object_permission(self, request, view, obj):
        if (request.method in permissions.SAFE_METHODS
                or obj.author == request.user):
            return True
        return request.user.is_admin

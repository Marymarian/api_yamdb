from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Доступ разрешен только администраторам"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == 'admin'))


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ на чтение разрешен всем, на изменение - администраторам"""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_superuser
                         or request.user.role == 'admin')))


class IsAdminAuthorOrReadOnly(permissions.BasePermission):
    """
    Доступ к чтению списков разрешен всем, изменению - авторизованным
    пользователям. Доступ к чтению объектов разрешен всем, к изменению -
    автору, модераторам или администраторам
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_superuser
                    or request.user.role == 'admin'
                    or request.user.role == 'moderator'
                    or obj.author == request.user))

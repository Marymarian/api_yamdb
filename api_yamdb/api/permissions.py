from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == 'Admin'))


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.is_superuser
                         or request.user.role == 'Admin')))


class IsAdminAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_superuser
                    or request.user.role == 'Admin'
                    or request.user.role == 'Moderator'
                    or obj.author == request.user))

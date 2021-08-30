from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method == 'PUT' and request.user.is_authenticated
            and obj.author == request.user
        )

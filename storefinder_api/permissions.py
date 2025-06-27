from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


"""
Alternative Owner od Admin can update/delete their store for future use for now it's just me using it


class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user and (request.user.is_staff or obj.owner == request.user)

"""
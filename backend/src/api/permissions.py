from rest_framework import permissions

class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,account):
        if request.user:
            return account==request.user
        return False


class IsOfferOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_client:
            return False
        return False
    def has_object_permission(self,request,view,order):
        if request.user:
            return order.owner==request.user
        return False



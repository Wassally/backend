from rest_framework import permissions

class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,account):
        if request.user:
            return account==request.user
        return False


class IsOfferOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,order):
        if request.user:
            return order.owner==request.user
        return False

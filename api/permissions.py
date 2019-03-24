from rest_framework import permissions

class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,account):
        if request.user:
            return account==request.user
        return False


class IsClientAndOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_client:
            return True
        return False
    def has_object_permission(self,request,view,package):
        if request.user==package.owner:
            return  package.state=="avaliable"
        return False





class IsOfferOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_captain:
            return True
        return False

    def has_object_permission(self, request, view, offer):
        if request.user.captain:
            return offer.owner == request.user.captain
        return False

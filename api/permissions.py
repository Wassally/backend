from rest_framework import permissions
from api.models import Delivery


class IsAccountOwner(permissions.BasePermission):
    def has_permission(self, request, view):

        return True

        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user:
            return account == request.user
        return False


class IsPostOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return request.user and request.user.is_authenticated


class IsClientAndOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "PATCH":
            return False

        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_client:
            return True

        return False

    def has_object_permission(self, request, view, package):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user == package.owner:
            try:
                delivery = Delivery.objects.get(package=package)
                return delivery.state == "phase1"
            except:
                return False
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

'''views for api to control'''

from rest_framework import permissions, viewsets
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.authentication import BasicAuthentication
from django.http import Http404
from django.contrib.auth import login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from accounts.serializers import (
    UserSerializer, PackageSerializer,
    OfferSerializer, ClientDeliverySerializer)
from accounts.models import User, Package, Offer
from .permissions import (IsAccountOwner, IsOfferOwner,
                          IsClientAndOwner)
from .authentication_class import (CsrfExemptSessionAuthentication,
                                   EmailOrUserNameModelBackend)

from .serializers import AuthTokenCustomSerializer


class AccountViewSet(viewsets.ModelViewSet):
    '''model view for account'''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAccountOwner]

    def destroy(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            self.perform_destroy(obj)
            return Response({"message": "the object was deleted"},
                            status=status.HTTP_204_NO_CONTENT)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
# packages


class PackageViewSet(viewsets.ModelViewSet):
    '''model view for package'''
    serializer_class = PackageSerializer
    queryset = Package.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsClientAndOwner)

    def destroy(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            self.perform_destroy(obj)
            return Response({"message": "the object was deleted"},
                            status=status.HTTP_204_NO_CONTENT)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
# custom list packages


class PackageCustomListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''model view for filtering backage'''

    serializer_class = PackageSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Package.objects.all()
        state = self.request.query_params.get("state", None)
        if state:
            if state in ["accepted", "avaliable"]:
                queryset = queryset.filter(state=state)
        return queryset

# offers

# not using this class any way -_____- right now


class OfferViewSet(viewsets.ModelViewSet):
    '''model view for offers'''

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticatedOrReadOnly(), IsOfferOwner())

    def destroy(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            self.perform_destroy(obj)
            return Response({"message": "the object was deleted"},
                            status=status.HTTP_204_NO_CONTENT)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


# delivery view for client
class ClientAcceptViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''model view for accepting client for offer'''

    serializer_class = ClientDeliverySerializer
    permission_classes = (permissions.IsAuthenticated,)


# login

class CustomAuthTokenLogin(ObtainAuthToken):
    '''custom authentication jwt'''
    serializer_class = AuthTokenCustomSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'auth_token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'name': user.username
        })

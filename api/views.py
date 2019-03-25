'''views for api to control'''

from rest_framework import permissions, viewsets
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.authentication import BasicAuthentication
from django.http import Http404
from django.contrib.auth import login, logout

from accounts.serializers import (
    UserSerializer, PackageSerializer, OfferSerializer, ClientDeliverySerializer)
from accounts.models import User, Package, Offer
from .permissions import IsAccountOwner, IsOfferOwner, IsClientAndOwner
from .authentication_class import CsrfExemptSessionAuthentication, EmailOrUserNameModelBackend


class AccountViewSet(viewsets.ModelViewSet):
    '''model view for account'''
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        if self.request.method == "POST":
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticatedOrReadOnly(), IsAccountOwner())

    def perform_create(self, serializer):
        account = serializer.save()
        login(self.request, account)

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
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = PackageSerializer
    queryset = Package.objects.all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticatedOrReadOnly(), IsClientAndOwner())

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
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
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


class OfferViewSet(viewsets.ModelViewSet):
    '''model view for offers'''
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
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
class ClientAcceptDeliveryViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''model view for accepting client for offer'''
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = ClientDeliverySerializer
    permission_classes = (permissions.IsAuthenticated,)


# login

class LoginView(views.APIView):
    '''model view for login'''
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        '''authentication with post request'''

        username = request.data.get("username")
        password = request.data.get("password")
        custom_authenticate = EmailOrUserNameModelBackend().authenticate
        # authenticate
        account = custom_authenticate(
            request, username=username, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)

                # serializing
                serializer = UserSerializer(account)
                return Response(serializer.data)
            else:
                return Response(
                    {'status': 'Unauthorized',
                     "message": 'this account has been disabled'},
                    status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(
                {'status': 'Unauthorized',
                 'message': 'Username/password invalid'},
                status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    '''model view for logout'''

    def get(self, request, format=None):
        '''loggin out with get'''
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

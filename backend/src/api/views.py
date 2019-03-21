from rest_framework import permissions ,viewsets
from accounts.serializers import UserSerializer, PackageSerializer, OfferSerializer
from  accounts.models import User,Captain,Package,Offer
from .permissions import IsAccountOwner, IsOfferOwner, IsClientAndOwner
from django.contrib.auth import authenticate, login ,logout
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from .Authentication_class import CsrfExemptSessionAuthentication
from django.http import Http404
from rest_framework import mixins



class AccountViewSet(viewsets.ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset=User.objects.all()
    serializer_class=UserSerializer
    

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        if self.request.method=="POST":
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticatedOrReadOnly(),IsAccountOwner())
    
    def destroy(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            self.perform_destroy(obj)
            return Response({"message": "the object was deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
#packages
class PackageViewSet(viewsets.ModelViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)  
    serializer_class=PackageSerializer
    queryset=Package.objects.all()
        
   

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        
        return (permissions.IsAuthenticatedOrReadOnly(), IsClientAndOwner())
        

    def destroy(self, request, *args, **kwargs):
        try :
            obj = self.get_object()
            self.perform_destroy(obj)
            return Response({"message": "the object was deleted"}, status=status.HTTP_204_NO_CONTENT)    
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
#custom list packages

class PackageCustomListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = PackageSerializer

    permission_classes = (permissions.IsAuthenticated,)


    def get_queryset(self):
        queryset = Package.objects.all()
        state=self.request.query_params.get("state",None)
        if state :
            if state in ["accepted","avaliable"]:
                queryset=queryset.filter(state=state)
        return queryset

#offers
class OfferViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset=Offer.objects.all()
    serializer_class=OfferSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticatedOrReadOnly(), IsOfferOwner())

    
    def destroy(self, request, *args, **kwargs):
        try :
            obj = self.get_object()
            self.perform_destroy(obj)
            return Response({"message": "the object was deleted"}, status=status.HTTP_204_NO_CONTENT)    
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

#login 

class LoginView(views.APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self,request,format=None):
        username=request.data.get("username")
        password=request.data.get("password")
        
        #authenticate
        account=authenticate(request,username=username,password=password)

        if account is not None:
            if account.is_active:
                login(request,account)

                #serializing
                serializer=UserSerializer(account)
                return Response(serializer.data)
            else:
                return Response(
                    {'status':'Unauthorized',
                    "message":'this account has been disabled'}
                   , status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status':'Unauthorized',
                'message':'Username/password invalid'},
                status=status.HTTP_401_UNAUTHORIZED
            )
class LogoutView(views.APIView):
    def get(self,request,format=None):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


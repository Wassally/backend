from rest_framework import permissions ,viewsets
from  accounts.serializers import UserSerializer,OrderPostSerializer
from  accounts.models import User,Captain,OrderPost
from .permissions  import IsAccountOwner,IsOfferOwner
from django.contrib.auth import authenticate, login ,logout
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from .Authentication_class import CsrfExemptSessionAuthentication



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
    
    def destroy(self,request,pk=None):
        obj=self.queryset.get(id=pk).delete()
        return Response({"message": "the object was deleted"}, status=status.HTTP_204_NO_CONTENT)
#order_post


class OrderPostViewSet(viewsets.ModelViewSet):
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    
    queryset=OrderPost.objects.all()
    serializer_class=OrderPostSerializer
    
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticatedOrReadOnly(), IsOfferOwner())



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


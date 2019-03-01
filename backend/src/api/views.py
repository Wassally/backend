from rest_framework import permissions ,viewsets
from  accounts.serializers import UserSerializer
from  accounts.models import User,Captain
from .permissions  import IsAccountOwner


class AccountViewSet(viewsets.ModelViewSet):

    queryset=User.objects.all()
    serializer_class=UserSerializer
    lookup_filed='username'

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        if self.request.method=="POST":
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticatedOrReadOnly(), IsAccountOwner())
    





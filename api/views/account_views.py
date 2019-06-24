from django.http import Http404
from rest_framework import viewsets
from rest_framework import status
from api.permissions import IsPostOrIsAuthenticated, IsAccountOwner
from api.serializers import UserSerializer, UserCreateSerializer
from api.models import User
from rest_framework.response import Response


class AccountViewSet(viewsets.ModelViewSet):
    '''model view for account'''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsPostOrIsAuthenticated, IsAccountOwner)

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == "POST":
            serializer_class = UserCreateSerializer
        return serializer_class

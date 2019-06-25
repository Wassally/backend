from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsPostOrIsAuthenticated, IsAccountOwner
from api.serializers import (UserSerializer,
                             UserCreateSerializer,
                             ResetPasswordSerializer)
from api.models import User


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


@api_view(['POSt'])
@permission_classes((IsAuthenticated, ))
def ResetPasswordViewSet(request):
    context = {"request": request}
    serializer = ResetPasswordSerializer(data=request.data, context=context)
    if serializer.is_valid():
        new_password = request.data['new_password']
        request.user.set_password(new_password)
        request.user.save()
        return Response("the password is updated",
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

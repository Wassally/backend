from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.serializers import ClientAddressEndPointSerializer
from api.permissions import IsAddressOwner
from api.models import Address


class ClientAddressViewSet(mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet
                           ):

    serializer_class = ClientAddressEndPointSerializer
    permission_classes = (IsAuthenticated, IsAddressOwner)
    queryset = Address.objects.all()

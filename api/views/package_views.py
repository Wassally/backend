from django.http import Http404
from rest_framework import permissions, viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsClientAndOwner
from api.serializers import PackageCreateSerializer, PackageUpdateSerializer
from api.models import Package

from ..filters import PackageFilter


class PackageViewSet(viewsets.ModelViewSet):
    '''model view for package'''
    serializer_class = PackageUpdateSerializer
    queryset = Package.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsClientAndOwner)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_class = PackageFilter

    ordering_fields = '__all__'

    filterset_fields = ('state',)

    def get_queryset(self):

        return self.queryset.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PackageCreateSerializer
        return self.serializer_class

from django.http import Http404
from rest_framework import permissions, viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsClientAndOwner
from api.serializers import PackageCreateSerializer, PackageUpdateSerializer
from api.models import Package


class PackageViewSet(viewsets.ModelViewSet):
    '''model view for package'''
    serializer_class = PackageUpdateSerializer
    queryset = Package.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsClientAndOwner)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    ordering_fields = '__all__'

    filterset_fields = ('state',)

    def get_queryset(self):

        return self.queryset.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PackageCreateSerializer
        return self.serializer_class

    def destroy(self, request, *args, **kwargs):
        print("yes")
        try:
            obj = self.get_object()
            self.perform_destroy(obj)
            return Response({"message": "the object was deleted"},
                            status=status.HTTP_204_NO_CONTENT)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

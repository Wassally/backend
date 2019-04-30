from rest_framework import permissions, viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from api.permissions import IsClientAndOwner
from api.serializers import PackageSerializer
from api.models import Package


class PackageViewSet(viewsets.ModelViewSet):
    '''model view for package'''
    serializer_class = PackageSerializer
    queryset = Package.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsClientAndOwner)
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    ordering_fields = '__all__'

    filterset_fields = ('state',)

    def get_queryset(self):

        return self.queryset.filter(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            self.perform_destroy(obj)
            return Response({"message": "the object was deleted"},
                            status=status.HTTP_204_NO_CONTENT)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

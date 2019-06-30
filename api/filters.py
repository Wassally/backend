import django_filters
from api.models import Package


class PackageFilter(django_filters.rest_framework.FilterSet):
    delivery_state = django_filters.CharFilter(
        field_name='delivery__state', lookup_expr='contains')

    class Meta:
        model = Package
        fields = ['delivery_state']

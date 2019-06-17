from rest_framework import serializers

from drf_extra_fields.geo_fields import PointField

from ..models import Address, PackageAddress


class AddressSerializer(serializers.ModelSerializer):
    ''' serializer for client address used ad a field '''

    location = PointField()

    class Meta:
        model = Address
        fields = ('location', 'governate', 'city')


class PackageAddressSerializer(serializers.ModelSerializer):
    ''' serializer for package address used as a field '''

    to_address = AddressSerializer(many=False)
    from_address = AddressSerializer(many=False)

    class Meta:
        model = PackageAddress
        fields = ('to_address', 'from_address')


#     class Meta:
#         model = PackageAddress
#         fields = ("client_address", "location", "governate", "city",
#                   "receiver_name", "receiver_phone_number")

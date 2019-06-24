from rest_framework import serializers

from drf_extra_fields.geo_fields import PointField

from ..models import Address, PackageAddress, ClientAddress


class AddressSerializer(serializers.ModelSerializer):
    ''' serializer for client address used ad a field '''

    location = PointField()

    class Meta:
        model = Address
        fields = ('id', 'formated_address', 'location', 'address_description')


class PackageAddressSerializer(serializers.ModelSerializer):
    ''' serializer for package address used as a field '''

    to_address = AddressSerializer()
    from_address = AddressSerializer()

    class Meta:
        model = PackageAddress
        fields = ('to_address', 'from_address')


class ClientAddressSerializer(serializers.ModelSerializer):
    ''' serializer for  client  address description used as a field '''

    address = AddressSerializer()

    class Meta:
        model = ClientAddress
        fields = ('address',)


class ClientAddressEndPointSerializer(AddressSerializer):
    ''' serializer for client Address  '''

    def create(self, validated_data):
        address = super().create(validated_data)
        user = self.context["request"].user
        ClientAddress.objects.create(user=user, address=address)

        return address

from django.db import transaction, IntegrityError
from django.utils.timesince import timesince


from rest_framework import serializers
from rest_framework import status

from drf_extra_fields.geo_fields import PointField

from api.models import Package, Delivery, Address, PackageAddress


from .address_serializer import AddressSerializer, PackageAddressSerializer


class PackageSerializer(serializers.ModelSerializer):
    '''Serializer for package.'''

    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()
    packageaddress = PackageAddressSerializer(many=False)

    class Meta:
        model = Package
        fields = ('id', 'owner', 'receiver_name', 'receiver_phone_number',
                  'note', 'weight', 'transport_way', 'duration',
                  'created_at', 'updated_at',
                  'time_since', "state", "wassally_salary", 'packageaddress')

        read_only_fields = ("created_at", "updated_at",
                            "state", "wassally_salary")

    default_error_messages = {
        'update_error': 'can not update package data',
        'create_error': 'can not create package '
    }

    def validate_packageaddress(self, value):
        ''' validation required for update so user can not 
        update city or governate only he must specify the location '''

        if value.get("to_address") and \
                not(value.get("to_address").get('location')):
            raise serializers.ValidationError(
                {"to_address": {"location": "this field is required"}})

        elif value.get("from_address").get('location') and \
                not (value.get("from_address").get('location')):
            raise serializers.ValidationError(
                {"from_address": {"location": "this field is required"}})

        return value

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d/%m/%Y")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%d/%m/%Y")

    def get_time_since(self, obj):
        return timesince(obj.created_at)

    def create(self, validated_data):

        try:
            return self.perform_create(validated_data)

        except IntegrityError:

            return self.fail('create_error')

    @transaction.atomic
    def perform_create(self, validated_data):
        ''' perform the creation of tables '''
        weight, transport_way, to_address, from_address = \
            self.cleaning_validated_data(validated_data)

        package = Package.objects.create(**validated_data)

        if validated_data["transport_way"] == "wassally":
            package.transport_way = "wassally"
            package.state = "pending"
            package.save()
            Delivery.objects.create(package=package, state="phase1")
            to_address, _ = Address.objects.get_or_create(**to_address)
            from_address, _ = Address.objects.get_or_create(**from_address)
            PackageAddress.objects.create(package=package,
                                          to_address=to_address,
                                          from_address=from_address
                                          )
        return package

    @transaction.atomic
    def update(self, instance, validated_data):
        weight, transport_way, to_address, from_address = \
            self.cleaning_validated_data(validated_data)

        if to_address:
            self.updating_address_model(instance, to_address)
        if from_address:
            self.updating_address_model(instance, from_address)

        instacne = super().update(instance, validated_data)

        return instacne

    def cleaning_validated_data(self, validated_data):
        ''' cleaning and parsing the validated data '''

        validated_data["owner"] = self.context["request"].user
        packageaddress = validated_data.pop('packageaddress', None)
        weight = validated_data.get("weight", None)
        transport_way = validated_data.get("transport_way", None)
        if packageaddress:
            to_address = packageaddress.get("to_address", None)
            from_address = packageaddress.get("from_address", None)
        else:
            to_address = None
            from_address = None
        return (weight, transport_way, to_address, from_address)

    def updating_address_model(self, instance,
                               from_address=None, to_address=None):
        ''' updating address model  '''

        if to_address:
            instacne_address = instance.packageaddress.to_address
            address = to_address
        elif from_address:
            instacne_address = instance.packageaddress.from_address
            address = from_address

        try:
            existed_add = Address.objects.get(location=address.get('location'))
            instacne_address = existed_add
            instacne_address.save()
            return instacne_address

        except Address.DoesNotExist:
            instacne_address.city = address.get('city', instacne_address.city)

            instacne_address.governate = address.get(
                'governate', instacne_address.governate)

            instacne_address.location = address.get(
                'location', instacne_address.location)

            instacne_address.save()
            return instacne_address

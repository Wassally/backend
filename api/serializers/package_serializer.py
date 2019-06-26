from django.db import transaction, IntegrityError
from django.utils.timesince import timesince


from rest_framework import serializers
from rest_framework import status

from drf_extra_fields.geo_fields import PointField

from geopy.distance import vincenty

from api.models import Package, Delivery, Address, PackageAddress


from .address_serializer import AddressSerializer, PackageAddressSerializer


class PackageSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()
    package_address = PackageAddressSerializer(many=False,
                                               source='packageaddress')

    class Meta:
        model = Package
        fields = ('id', 'owner', 'sender_phone_number', 'receiver_name',
                  'receiver_phone_number', 'note', 'weight', 'transport_way',
                  'duration', 'created_at', 'updated_at', 'time_since',
                  "state", "wassally_salary", 'package_address')

        read_only_fields = ("created_at", "updated_at",
                            "state", "wassally_salary")

    default_error_messages = {
        'update_error': 'can not update package data',
        'create_error': 'can not create package '
    }

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d/%m/%Y")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%d/%m/%Y")

    def get_time_since(self, obj):
        return timesince(obj.created_at)

    def cleaning_validated_data(self, validated_data):
        ''' cleaning and parsing the validated data '''

        validated_data["owner"] = self.context["request"].user
        weight = validated_data.get("weight", None)
        transport_way = validated_data.get("transport_way", None)
        package_address = validated_data.pop("packageaddress", None)

        if package_address:
            to_address = package_address.get('to_address', None)
            from_address = package_address.get('from_address', None)
        else:
            to_address = None
            from_address = None

        return (weight, transport_way, to_address, from_address)

    @staticmethod
    def distance_between_points(point1, point2):
        distance = vincenty(point1.coords, point2.coords).kilometers
        if distance < 2:
            raise serializers.ValidationError(
                {"message": 'the distance should be grater than 2 km'})
        return True


class PackageCreateSerializer(PackageSerializer):
    '''Serializer for package.'''

    def validate(self, attrs):

        from_address_location = attrs.get('packageaddress').get(
            'from_address').get('location')

        to_address_location = attrs.get('packageaddress').get(
            'to_address').get('location')

        self.distance_between_points(
            from_address_location, to_address_location)

        return attrs

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

        to_address = Address.objects.create(**to_address)
        from_address = Address.objects.create(**from_address)
        PackageAddress.objects.create(to_address=to_address,
                                      from_address=from_address,
                                      package=package)
        return package


class PackageUpdateSerializer (PackageSerializer):
    class Meta:
        model = Package
        fields = ('id', 'owner', 'sender_phone_number', 'receiver_name',
                  'receiver_phone_number', 'note', 'weight',
                  'duration', 'created_at', 'updated_at', 'time_since',
                  "state", "wassally_salary", 'package_address')

        read_only_fields = ("created_at", "updated_at",
                            "state", "wassally_salary")

    @transaction.atomic
    def update(self, instance, validated_data):

        weight, transport_way, to_address, from_address = \
            self.cleaning_validated_data(validated_data)

        instacne = super().update(instance, validated_data)

        if to_address:
            self.updating_address_model(instacne, to_address=to_address)
        if from_address:
            self.updating_address_model(instance, from_address=from_address)

        if to_address or from_address:
            self.distance_between_points(
                instacne.packageaddress.to_address.location,
                instacne.packageaddress.from_address.location
            )
            instacne.packageaddress.to_address.save()
            instacne.packageaddress.from_address.save()
            instacne.save()

        return instacne

    def updating_address_model(self, package,
                               to_address=None, from_address=None):

        if to_address:
            address = to_address
            instace_address = package.packageaddress.to_address
        elif from_address:
            address = from_address
            instace_address = package.packageaddress.from_address

        instace_address.formated_address = address.get(
            'formated_address', instace_address.formated_address)

        instace_address.location = address.get(
            'location', instace_address.location)

        instace_address.address_description = address.get(
            'address_description', instace_address.address_description)

        return instace_address


class ComputingSalarySerializer(serializers.Serializer):
    ''' serializer for validating fields of the function '''

    to_formated_address = serializers.CharField(required=True)
    from_formated_address = serializers.CharField(required=True)
    weight = serializers.IntegerField(required=True)
    from_location = PointField(required=True)
    to_location = PointField(required=True)

    def validate(self, attrs):

        to_location = attrs["to_location"]
        from_location = attrs["from_location"]
        PackageSerializer.distance_between_points(to_location, from_location)
        return attrs

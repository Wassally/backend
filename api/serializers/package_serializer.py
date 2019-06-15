from rest_framework import serializers
from rest_framework import status
from drf_extra_fields.geo_fields import PointField
from django.db import transaction
from django.utils.timesince import timesince
from api.models import Package, Delivery
from api.logic import computing_salary


class PackageSerializer(serializers.ModelSerializer):
    '''Serializer for package.'''

    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()
    to_location = PointField()
    from_location = PointField()

    class Meta:
        model = Package
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at",
                            "state", "wassally_salary")

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d/%m/%Y")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%d/%m/%Y")

    def get_time_since(self, obj):
        return timesince(obj.created_at)

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        # wassally_salary = validated_data["wassally_salary"]
        to_location = validated_data["to_location"]
        from_location = validated_data["from_location"]
        weight = validated_data["weight"]
        transport_way = validated_data["transport_way"]
        expected_salary = computing_salary(to_location, from_location, weight)

        package = Package.objects.create(**validated_data)

        if validated_data["transport_way"] == "wassally":
            package.wassally_salary = expected_salary
            package.transport_way = "wassally"
            package.state = "pending"
            package.save()
            Delivery.objects.create(package=package, state="phase1")

        return package

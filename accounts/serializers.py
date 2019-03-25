'''Serializer for accounts.'''
from rest_framework import serializers
<<<<<<< HEAD
from rest_framework.validators import UniqueValidator
=======
>>>>>>> 2160ecf... modyfiy serializer.py to meet pylint spec
from django.contrib.auth import update_session_auth_hash
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from .models import User, Captain, Package, Delivery, Offer


class OfferSerializer(serializers.ModelSerializer):
    '''Serializer for offer system.'''

    package = serializers.SlugRelatedField(
        queryset=Package.objects.filter(state="avaliable"), slug_field="id")

    class Meta:
        model = Offer
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "owner")
        depth = 1

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user.captain
        offer = Offer.objects.create(**validated_data)
        return offer
# creating custom offer serializer for special use for not including package on in it


class OfferCustomSerializer(serializers.ModelSerializer):
    '''Custom serializer for represent package in a good way'''
    class Meta:
        model = Offer
        exclude = ("package",)
        read_only_fields = ("created_at", "updated_at", "owner")
        depth = 1
# Package serializer


class PackageSerializer(serializers.ModelSerializer):
    '''Serializer for package.'''

    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    related_offers = OfferCustomSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "state")

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        package = Package.objects.create(**validated_data)
        return package


# captain serializer

class CaptainSerializer(serializers.ModelSerializer):
    '''Serializer for Captain'''
    national_id = serializers.IntegerField(required=False)
    image_national_id = Base64ImageField(required=False)

    class Meta:
        model = Captain
        exclude = ("user",)
        depth = 2


class ClientDeliverySerializer(serializers.ModelSerializer):
    '''serializer for clients to accept offer and putting it in delvery model.'''

    def get_fields(self):
        fields = super().get_fields()
        fields['package'].queryset = Package.objects.filter(
            state="avaliable", owner=self.context["request"].user)
        captains = fields['package'].queryset.values_list(
            "related_offers__owner__id", flat=True)
        fields['captain'].queryset = Captain.objects.filter(id__in=captains)
        return fields

    class Meta:
        model = Delivery
        fields = "__all__"
        read_only_fields = ("state",)


# user serializer
class UserSerializer(serializers.ModelSerializer):
    '''Serializer for user.'''
    captain = CaptainSerializer(required=False)
<<<<<<< HEAD
    password = serializers.CharField(write_only=True)
    image = Base64ImageField(required=False)
    password_updated_message = serializers.SerializerMethodField()
    packages = PackageSerializer(many=True, read_only=True)
    email = serializers.EmailField(allow_blank=False, required=True,
                                   validators=[UniqueValidator(queryset=User.objects.all())])
=======
    password = serializers.CharField(write_only=True, required=False)
    image = Base64ImageField(required=False)
    password_updated_message = serializers.SerializerMethodField()
    packages = PackageSerializer(many=True, read_only=True)
>>>>>>> 2160ecf... modyfiy serializer.py to meet pylint spec

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password', "password_updated_message",
                  'is_captain', 'is_client', "governate", "city", "phone_number",
                  'captain', "image", "packages")
        read_only_fields = ("created_at", "updated_at")

    # function for insertinf filed message to insure that password was updated
    def get_password_updated_message(self, obj):
        '''validate on message filed for updating password'''
        try:
            self.initial_data
        except AttributeError:
            return None
        if not self.initial_data.get("password", None):
            return "password not updated"
        return "password updated successfully"

    @transaction.atomic
    def create(self, validated_data):
        captain_confirm = validated_data.pop("captain", None)
        if validated_data.get("is_client"):
            return User.objects.create_user(**validated_data)
        elif validated_data.get("is_captain"):
            user = User.objects.create_user(**validated_data)
            if captain_confirm:
                Captain.objects.create(user=user, **captain_confirm)
                return user

    @transaction.atomic
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        captain_data = validated_data.pop("captain", None)
        if instance.is_client:
            instance = super().update(instance, validated_data)
<<<<<<< HEAD
            # sure is captain is false
=======
            #sure is captain is false
>>>>>>> 2160ecf... modyfiy serializer.py to meet pylint spec
            instance.is_captain = False
            instance.save()

        elif instance.is_captain:
            instance = super().update(instance, validated_data)
            captain = instance.captain
            # this if cuz we might give captain data with out suppling captain filed
            if captain_data:
                captain.national_id = captain_data.get(
                    "national_id", captain.national_id)
                captain.feedback = captain_data.get(
                    "feedback", captain.feedback)
                captain.save()
            # sure is_client is false
            instance.is_client = False
            instance.save()

        # updating_password_if_these_conditions_only
        if password:
            instance.set_password(password)
            instance.save()
            update_session_auth_hash(self.context['request'], instance)

        return instance

# order_post serializer


# class SlugRelatedCustomField(serializers.SlugRelatedField):
#     def get_queryset(self):
#         queryset=self.queryset
#         orders_in_delivery = queryset.values_list("order")
#         if hasattr(self.root,id):
#             queryset=queryset.exclude(order__in=orders_in_delivery)
#             return queryset

# class DeliverySerializer(serializers.ModelSerializer):
#     order=serializers.SlugRelatedCustomField(queryset=Package.objcts.all(),slug_field="id")
#     class Meta:
#         model=Delivery
#         fields="__all__"

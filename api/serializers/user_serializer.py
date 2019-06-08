from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from rest_framework import status
from drf_extra_fields.fields import Base64ImageField
from django.contrib.auth import update_session_auth_hash
from django.db import transaction
from api.models import User, Captain
from .package_serializer import PackageSerializer


class CaptainSerializer(serializers.ModelSerializer):
    '''Serializer for Captain'''
    national_id = serializers.IntegerField(required=False)
    image_national_id = Base64ImageField(required=False)

    class Meta:
        model = Captain
        exclude = ("user",)
        depth = 2


class UserSerializer(serializers.ModelSerializer):
    '''Serializer for user.'''
    captain = CaptainSerializer(required=False)
    password = serializers.CharField(write_only=True)
    image = Base64ImageField(required=False)
    packages = PackageSerializer(many=True, read_only=True)
    email = serializers.EmailField(
        allow_blank=False, required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    is_captain = serializers.BooleanField(required=True)
    is_client = serializers.BooleanField(required=True)
    governate = serializers.CharField(required=False)
    city = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'created_at',
            'updated_at', 'first_name', 'last_name', 'password',
            'is_captain', 'is_client', "governate", "city",
            "phone_number", 'captain', "image", "packages")
        read_only_fields = ("created_at", "updated_at")

    @transaction.atomic
    def create(self, validated_data):
        captain_confirm = validated_data.pop("captain", None)
        if validated_data.get("is_client") == validated_data.get("is_captain"):
            raise serializers.ValidationError("must be captain or client")
        elif validated_data.get("is_client"):
            user = User.objects.create_user(**validated_data)
        elif validated_data.get("is_captain"):
            user = User.objects.create_user(**validated_data)
            if captain_confirm:
                Captain.objects.create(user=user, **captain_confirm)
            else:
                raise serializers.ValidationError(
                    "set national id at least for the captain")
        Token.objects.create(user=user)
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        captain_data = validated_data.pop("captain", None)
        if instance.is_client:
            instance = super().update(instance, validated_data)
            instance.is_captain = False
            instance.is_client = True
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
            instance.is_captain = True
            instance.save()

        # updating_password_if_these_conditions_only
        if password:
            instance.set_password(password)
            instance.save()

        return instance


class UserCreateSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'id', "auth_token", 'email', 'username', 'created_at',
            'updated_at', 'first_name', 'last_name', 'password',
            'is_captain', 'is_client', "governate", "city",
            "phone_number", 'captain', "image", "packages")
        read_only_fields = ("created_at", "updated_at", "auth_token")

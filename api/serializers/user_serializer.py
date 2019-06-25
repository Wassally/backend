from django.db import transaction, IntegrityError
from django.core import exceptions as django_exceptions
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.fields import CurrentUserDefault

from drf_extra_fields.fields import Base64ImageField


from api.models import User, Captain, Address, ClientAddress
from . import PackageSerializer
from .address_serializer import ClientAddressSerializer


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
    image = Base64ImageField(required=False)
    packages = PackageSerializer(many=True, read_only=True)
    email = serializers.EmailField(
        allow_blank=False, required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    is_captain = serializers.BooleanField(required=True)
    is_client = serializers.BooleanField(required=True)
    user_addresses = ClientAddressSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'created_at',
            'updated_at', 'first_name', 'last_name', 'phone_number',
            'is_captain', 'is_client', 'user_addresses',
            'captain', "image", "packages")
        read_only_fields = ("created_at", "updated_at",
                            'is_captain', 'is_client')

    default_error_messages = {
        'update_error': 'can not update user data',
        'create_error': 'can not create user '
    }

    def update(self, instance, validated_data):

        try:
            instance = self.perform_update(instance, validated_data)

        except IntegrityError:
            self.fail('update_error')

        return instance

    @transaction.atomic
    def perform_update(self, instance, validated_data):
        captain_data = validated_data.pop("captain", None)

        if instance.is_client:
            instance = super().update(instance, validated_data)

        elif instance.is_captain:
            instance = super().update(instance, validated_data)
            captain = instance.captain
    # this if cuz we might give captain data with out suppling captain filed
            if captain_data:
                captain.national_id = captain_data.get(
                    "national_id", captain.national_id)
                captain.vehicle = captain_data.get(
                    "feedback", captain.vehicle)
                captain.image_national_id = captain_data.get(
                    "image_national_id", captain.image_national_id)
                captain.save()

        return instance


class UserCreateSerializer(UserSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            'id', "auth_token", 'email', 'username', 'created_at',
            'updated_at', 'first_name', 'last_name', 'password',
            'phone_number', 'is_captain', 'is_client', 'user_addresses',
            'captain', "image", "packages")
        read_only_fields = ("created_at", "updated_at",
                            "auth_token")
        write_only_fields = ('password',)

    def validate(self, attrs):
        captain = attrs.pop('captain', None)
        user = User(**attrs)
        password = attrs.get('password')
        attrs['captain'] = captain

        try:
            validate_password(password, user)

        except django_exceptions.ValidationError as e:
            serializer_errors = serializers.as_serializer_error(e)
            raise serializers.ValidationError({
                'password': serializer_errors[
                    api_settings.NON_FIELD_ERRORS_KEY]
            })

        is_client = attrs.get('is_client')
        is_captain = attrs.get('is_captain')
        if is_captain == is_client:
            raise serializers.ValidationError("must be captain or client")

        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except serializers.ValidationError as e:
            return (e)

        except IntegrityError as e:
            self.fail('create_error')

        return user

    @transaction.atomic
    def perform_create(self, validated_data):

        captain_data = validated_data.pop("captain", None)
        user_addresses = validated_data.pop('user_addresses', None)

        if validated_data.get("is_client"):
            user = User.objects.create_user(**validated_data)
        elif validated_data.get("is_captain"):
            user = User.objects.create_user(**validated_data)
            if captain_data:
                Captain.objects.create(user=user, **captain_data)
            else:
                raise serializers.ValidationError(
                    "set national id at least for the captain")
        Token.objects.create(user=user)

        return user


class ResetPasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = self.context["request"].user
        old_password = attrs['old_password']
        new_password = attrs['new_password']

        if user.check_password(old_password):

            try:
                validate_password(new_password, user)

            except django_exceptions.ValidationError as e:
                serializer_errors = serializers.as_serializer_error(e)
                raise serializers.ValidationError({
                    'new_password': serializer_errors[
                        api_settings.NON_FIELD_ERRORS_KEY]
                })
        else:
            raise serializers.ValidationError({
                'old_password': 'wrong password try again'
            })
        return attrs

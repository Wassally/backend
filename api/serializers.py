'''serializer for custom authentication for
username or email using token authentication'''

from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.utils.translation import ugettext_lazy as _
from .authentication_class import EmailOrUserNameModelBackend


class AuthTokenCustomSerializer (AuthTokenSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            custom_authenticate = EmailOrUserNameModelBackend().authenticate
            user = custom_authenticate(request=self.context.get('request'),
                                       username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs

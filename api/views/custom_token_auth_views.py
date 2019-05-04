from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from api.serializers import AuthTokenCustomSerializer


class CustomAuthTokenLogin(ObtainAuthToken):
    '''custom authentication jwt'''
    serializer_class = AuthTokenCustomSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'auth_token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'name': user.username
        })

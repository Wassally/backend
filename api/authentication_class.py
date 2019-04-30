'''authentications backends'''
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class CsrfExemptSessionAuthentication(SessionAuthentication):
    ''' To not perform the csrf check previously happening'''

    def enforce_csrf(self, request):
        return


class EmailOrUserNameModelBackend(ModelBackend):
    '''Authenticate with username or password'''

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()
        if username is not None:
            users = user_model.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username))

        for user in users:
            if user.check_password(password):
                return user
        if not users:
            '''this line for reducing time between existing
             user and none existing user'''
            user_model().set_password(password)

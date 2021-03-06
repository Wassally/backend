from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''base user for both client and captain'''
    phone_number = models.CharField(max_length=14)
    is_captain = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='personal/%y/%m/', default="default.png")

    def __str__(self):
        return "%d: %s" % (self.id, self.username)


class Captain(models.Model):
    '''Extend user for captin object.'''

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vehicle = models.CharField(max_length=30, default="car")

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'api'

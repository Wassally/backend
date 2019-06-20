from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    '''base user for both client and captain'''

    is_captain = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    governate = models.CharField(max_length=40)
    city = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to='personal/%y/%m/', default="default.png")

    def __str__(self):
        return "%d: %s" % (self.id, self.username)


class Captain(models.Model):
    '''Extend user for captin object.'''

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.IntegerField()
    image_national_id = models.ImageField(
        upload_to='national_id/%y%m%d/', blank=True, null=True)
    vehicle = models.CharField(max_length=30, default="car")

    def __str__(self):
        return self.user.username

    class Meta:
        app_label = 'api'

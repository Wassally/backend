from django.contrib.gis.db import models
from . import User, Package
from django.contrib.gis.geos import Point


class Address(models.Model):
    ''' model for saving location'''

    address_description = models.CharField(
        max_length=50, null=True, blank=True)
    formated_address = models.CharField(max_length=100, null=True, blank=True)
    location = models.PointField()


class ClientAddress(models.Model):
    ''' model for client address'''
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='user_addresses')
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class PackageAddress(models.Model):

    ''' model for saving the address of package '''
    package = models.OneToOneField(Package, on_delete=models.CASCADE)
    from_address = models.ForeignKey(
        Address, related_name="fromaddress", on_delete=models.CASCADE)
    to_address = models.ForeignKey(
        Address, related_name="toaddress", on_delete=models.CASCADE, default=1)

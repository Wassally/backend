from django.contrib.gis.db import models
from . import User, Package


class Address(models.Model):
    ''' model for saving location'''

    governate = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=40, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    location = models.PointField(unique=True, null=True)
    clients = models.ManyToManyField(User, through="ClientAddress")


class ClientAddress(models.Model):
    ''' Through Table for m2m '''
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class PackageAddress(models.Model):

    ''' model for saving the address of package '''
    package = models.OneToOneField(Package, on_delete=models.CASCADE)
    from_address = models.ForeignKey(
        Address, related_name="fromaddress", on_delete=models.CASCADE)
    to_address = models.ForeignKey(
        Address, related_name="toaddress", on_delete=models.CASCADE)

from django.contrib.gis.db import models
from . import User, Package


class SourceAddress(models.Model):
    ''' abstract base model for main filed of address '''

    governate = models.CharField(max_length=40, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    location = models.PointField(srid=4326)

    class Meta:
        abstract = True


class DestinationAddress(SourceAddress):
    ''' abstract base model for main filed of destination address '''

    receiver_name = models.CharField(max_length=40)
    receiver_phone_number = models.CharField(max_length=14)

    class Meta:
        abstract = True


class ClientAddress(SourceAddress):
    ''' model for saving location of  user '''

    client = models.ForeignKey(
        User, related_name="address", on_delete=models.CASCADE)


class PackageAddress(DestinationAddress):
    ''' model for saving the address of package '''

    client_address = models.ForeignKey(
        ClientAddress, related_name="from_address", on_delete=models.CASCADE)
    package = models.ForeignKey(
        Package, related_name="package_address", on_delete=models.CASCADE)

    class Meta:
        unique_together = ['client_address', 'package']

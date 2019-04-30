from django.contrib.gis.geos import Point
from django.contrib.gis.db import models

from .user_model import User


class Package(models.Model):
    '''Package that client creates'''
    s = (("avaliable", "avaliable"),
         ("pending", "pending"))

    t = (("wassally", "wassally"),
         ("other", "other"))

    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name="packages")
    from_place = models.CharField(max_length=40)
    to_place = models.CharField(max_length=40)
    to_person = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.CharField(max_length=250, default="no note")
    duration = models.CharField(default="Not Specified", max_length=50)
    wassally_salary = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    state = models.CharField(choices=s, max_length=10, default="avaliable")
    transport_way = models.CharField(
        choices=t, max_length=9)
    to_location = models.PointField(srid=4326, null=True, blank=True)
    from_location = models.PointField(srid=4326, null=True, blank=True)

    def __str__(self):
        return self.note

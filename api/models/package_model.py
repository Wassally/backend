from django.contrib.gis.geos import Point
from django.db import models

from .user_model import User

from api.utils import computing_salary


class Package(models.Model):
    '''Package that client creates'''
    s = (("avaliable", "avaliable"),
         ("pending", "pending"))

    t = (("wassally", "wassally"),
         ("other", "other"))

    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name="packages")

    receiver_phone_number = models.CharField(max_length=14)
    sender_phone_number = models.CharField(max_length=14)

    receiver_name = models.CharField(max_length=20, default="fffff")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.CharField(max_length=250, default="no note")
    wassally_salary = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    state = models.CharField(choices=s, max_length=10, default="avaliable")
    transport_way = models.CharField(
        choices=t, max_length=9)

    duration = models.IntegerField()

    def __str__(self):
        return self.note

    def save(self, * args, **kwargs):
        self.wassally_salary = 0
        super().save(* args, **kwargs)

    class Meta:
        app_label = 'api'

from django.db import models
from .package_model import Package
from .user_model import Captain


class Delivery(models.Model):
    '''This model shows te delivery opeartion.'''
    s = (("waiting", "waiting"),
         ("delivered", "delivered"),
         ("shipping", "shipping"),
         ("shipped", "shipped"))
    package = models.OneToOneField(Package, on_delete=models.CASCADE)
    captain = models.ForeignKey(
        Captain, on_delete=models.CASCADE, related_name="captains", default=1)
    state = models.CharField(choices=s, max_length=11, default="waiting")

    ''' making cap and order unique and
    making that table for better manipulating with database'''
    class Meta:
        unique_together = (("package", "captain"),)
        app_label = 'api'

    def __str__(self):
        return f"order:{self.package} taken by captian{self.captain}"

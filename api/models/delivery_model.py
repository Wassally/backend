from django.contrib.gis.db import models
from .package_model import Package
from .user_model import Captain


class Delivery(models.Model):
    '''This model shows te delivery opeartion.'''
    s = (("phase1", "phase1"),
         ("phase2", "phase2"),
         ("phase3", "phase3"))
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="orders", default=0)
    captain = models.ForeignKey(
        Captain, on_delete=models.PROTECT, related_name="captains", null=True)
    state = models.CharField(choices=s, max_length=7, default="phase1")

    ''' making cap and order unique and
    making that table for better manipulating with database'''
    class Meta:
        unique_together = (("package", "captain"),)
        app_label = 'api'

    def __str__(self):
        return "order:%s taken by captian:%s" % (self.package, self.captain)

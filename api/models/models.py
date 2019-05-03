# '''Models for creating tables for account.'''

# from django.contrib.auth.models import AbstractUser
# from django.contrib.gis.db import models
# from django.core.validators import MaxValueValidator, MinValueValidator
# from django.contrib.gis.geos import Point


# class User(AbstractUser):
#     '''base user for both client and captain'''

#     is_captain = models.BooleanField(default=False)
#     is_client = models.BooleanField(default=False)
#     governate = models.CharField(max_length=40)
#     city = models.CharField(max_length=40)
#     phone_number = models.CharField(default="0", max_length=14)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     image = models.ImageField(
#         upload_to='personal/%y/%m/', default="default.png")

#     def __str__(self):
#         return "%d: %s" % (self.id, self.username)


# class Captain(models.Model):
#     '''Extend user for captin object.'''

#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     national_id = models.IntegerField()
#     image_national_id = models.ImageField(
#         upload_to='national_id/%y%m%d/', blank=True, null=True)
#     vehicle = models.CharField(max_length=30, default="car")

#     def __str__(self):
#         return self.user.username


# class Package(models.Model):
#     '''Package that client creates'''
#     s = (("avaliable", "avaliable"),
#          ("pending", "pending"))

#     t = (("wassally", "wassally"),
#          ("other", "other"))

#     owner = models.ForeignKey(User, on_delete=models.CASCADE,
#                               related_name="packages")
#     from_place = models.CharField(max_length=40)
#     to_place = models.CharField(max_length=40)
#     to_person = models.CharField(max_length=10)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     note = models.CharField(max_length=250, default="no note")
#     duration = models.CharField(default="Not Specified", max_length=50)
#     wassally_salary = models.IntegerField(default=0)
#     weight = models.IntegerField(default=0)
#     state = models.CharField(choices=s, max_length=10, default="avaliable")
#     transport_way = models.CharField(
#         choices=t, max_length=9)
#     to_location = models.PointField(srid=4326, null=True, blank=True)
#     from_location = models.PointField(srid=4326, null=True, blank=True)

#     def __str__(self):
#         return self.note


# class Delivery(models.Model):
#     '''This model shows te delivery opeartion.'''
#     s = (("phase1", "phase1"),
#          ("phase2", "phase2"),
#          ("phase3", "phase3"))
#     package = models.ForeignKey(
#         Package, on_delete=models.CASCADE, related_name="orders", default=0)
#     captain = models.ForeignKey(
#         Captain, on_delete=models.PROTECT, related_name="captains", null=True)
#     state = models.CharField(choices=s, max_length=7, default="phase1")

#     ''' making cap and order unique and
#     making that table for better manipulating with database'''
#     class Meta:
#         unique_together = (("package", "captain"),)
#         app_name = 'api'

#     def __str__(self):
#         return "order:%s taken by captian:%s" % (self.package, self.captain)


# class Offer(models.Model):
#     '''Model offer that captain makes.'''
#     owner = models.ForeignKey(
#         Captain, on_delete=models.CASCADE, related_name="offers")
#     text = models.CharField(max_length=250)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     offer_money = models.IntegerField()
#     package = models.ForeignKey(
#         Package, on_delete=models.CASCADE, related_name="related_offers")

#     def __str__(self):
#         return "there is money_offer(%d) from captian %s" %\
#             (self.offer_money, self.owner.user.username)


# class FeedBack(models.Model):
#     '''Feed back from clients to captains'''
#     client = models.ForeignKey(User, on_delete=models.CASCADE,
#                                related_name="client_feedback", )
#     captain = models.ForeignKey(
#         Captain, on_delete=models.CASCADE, related_name="captain_feedback")
#     text = models.CharField(max_length=250, default="no feedback")
#     rating = models.IntegerField(default=0, validators=[
#         MaxValueValidator(10), MinValueValidator(0)])

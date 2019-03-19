from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError





class User(AbstractUser):
    
    is_captain= models.BooleanField(default=False)
    is_client= models.BooleanField(default=False)
    governate=models.CharField(max_length=40)
    city=models.CharField(max_length=40)
    phone_number = models.IntegerField(blank=True,default=6545)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to='personal/%y/%m/',blank=True,null=True)

    def __str__(self):
        return "%d: %s" %(self.id,self.username)



class Captain(models.Model):
    
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    national_id=models.IntegerField()
    image_national_id = models.ImageField(
        upload_to='national_id/%y%m%d/', blank=True, null=True)
    vehicle = models.CharField(max_length=30,default="car")



    def __str__(self):
        return self.user.username
    


class Package(models.Model):
    s = (("p", "pending"),
         ("i", 'in_progress'),
         ("f", "finished"))
    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name="packages")
    from_place = models.CharField(max_length=40)
    to_place = models.CharField(max_length=40)
    to_person=models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    note = models.CharField(max_length=250,default="no note")
    time_day = models.IntegerField(default=0)
    time_hours = models.IntegerField(default=0, 
                validators=[MaxValueValidator(24)])
    time_minutes = models.IntegerField(
        default=0, validators=[MaxValueValidator(60)])
    offer_money = models.IntegerField()
    weight=models.IntegerField(default=0)
    state = models.CharField(choices=s, max_length=1, default="p")
    def __str__(self):
        return self.note


class Delivery(models.Model):
    
    package=models.ForeignKey(Package,on_delete=models.CASCADE,related_name="orders",default=0)
    captain=models.ForeignKey(Captain,on_delete=models.CASCADE,related_name="captains")
    
    
    #making cap and order unique and making that table for better manipulating with database
    class Meta:
        unique_together=(("package","captain"),)
    def __str__(self):
        return "order:%s taken by captian:%s"%(self.package,self.captain)


class Offer(models.Model):
    owner=models.ForeignKey(Captain,on_delete=models.CASCADE,related_name="offers")
    text=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    offer_money = models.IntegerField()
    package=models.ForeignKey(Package,on_delete=models.CASCADE,related_name="related_offers")


    def __str__(self):
        return "there is money_offer(%d) from captian %s"%(self.offer_money,self.owner.user.username) 





class FeedBack(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="client_feedback", )
    captain = models.ForeignKey(Captain, on_delete=models.CASCADE, related_name="captain_feedback")
    text=models.CharField(max_length=250,default="no feedback")
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(10),MinValueValidator(0)])




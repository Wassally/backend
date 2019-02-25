from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    
    is_captain= models.BooleanField(default=False)
    is_client= models.BooleanField(default=False)
    governate=models.CharField(max_length=40)
    city=models.CharField(max_length=40)
    phone_number = models.IntegerField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to='personal/%y/%m/',blank=True,null=True)



class Captain(models.Model):
    user=models.OneToOneField(User,primary_key=models.CASCADE,on_delete=True)
    national_id=models.IntegerField()
    image_national_id=models.ImageField(upload_to='national_id/%y%m%d/')
    feedback=models.CharField(max_length=250)



    def __str__(self):
        return self.user.username
    
class OrderPOSt(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")
    from_place = models.CharField(max_length=40)
    to_place = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250)
    time = models.CharField(max_length=40)
    offer_money = models.IntegerField()

    def __str__(self):
        return self.description

class Delivery(models.Model):
    s=(("w","waiting"),
        ("p",'progressing'),
        ("f","finished"))
    order=models.ForeignKey(OrderPOSt,on_delete=models.CASCADE,related_name="orders",unique=True)
    captain=models.ForeignKey(Captain,on_delete=models.CASCADE,related_name="captains")
    state = models.CharField(choices=s, max_length=1,default="w")

    def __str__(self):
        return "order:%s taken by captian:%s"%(self.order,self.captain)

class Offer(models.Model):
    owner=models.ForeignKey(Captain,on_delete=models.CASCADE,related_name="offers")
    text=models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    offer_money = models.IntegerField()
    orderpost=models.ForeignKey(OrderPOSt,on_delete=models.CASCADE,related_name="postoffers")


    def __str__(self):
        return "%s from: %s"%(self.text,self.owner) 


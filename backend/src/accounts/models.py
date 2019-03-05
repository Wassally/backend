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
    phone_number = models.IntegerField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to='personal/%y/%m/',blank=True,null=True)



class Captain(models.Model):
    
    user=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    national_id=models.IntegerField()
    image_national_id = models.ImageField(
        upload_to='national_id/%y%m%d/', blank=True, null=True)
    feedback=models.CharField(max_length=250)
    vehicle = models.CharField(max_length=30,default="car")



    def __str__(self):
        return self.user.username
    


class OrderPOSt(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orders")
    from_place = models.CharField(max_length=40)
    to_place = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=250)
    time_day = models.IntegerField(default=0)
    time_hours = models.IntegerField(default=0, 
                validators=[MaxValueValidator(24)])
    time_minutes = models.IntegerField(
        default=0, validators=[MaxValueValidator(60)])
    offer_money = models.IntegerField()

    def __str__(self):
        return self.description


class Delivery(models.Model):
    s=(("w","waiting"),
        ("p",'progressing'),
        ("f","finished"))
    order=models.ForeignKey(OrderPOSt,on_delete=models.CASCADE,related_name="orders")
    captain=models.ForeignKey(Captain,on_delete=models.CASCADE,related_name="captains")
    state = models.CharField(choices=s, max_length=1,default="w")
    
    #making cap and order unique and making that table for better manipulating with database
    class Meta:
        unique_together=(("order","captain"),)
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


#validator wii come back to imports later xd
def user_not_client(value):
    if not(User.objects.get(id=value).is_client):
        raise ValidationError("must be client")


class FeedBack(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="client_feedback", validators=[user_not_client])
    captain = models.ForeignKey(Captain, on_delete=models.CASCADE, related_name="captain_feedback")
    text=models.CharField(max_length=250,default="no feedback")
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(10),MinValueValidator(0)])




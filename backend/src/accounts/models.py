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
    

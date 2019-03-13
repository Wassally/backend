from rest_framework import serializers
from .models import User,Captain,OrderPost
from django.contrib.auth import update_session_auth_hash
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField

class CaptainSerializer(serializers.ModelSerializer):
    
    national_id = serializers.IntegerField(required=False)
    image_national_id = Base64ImageField(required=False)

    
    class Meta:
        model=Captain
        fields = ('national_id', "vehicle","image_national_id")


class OrderPostSerializer(serializers.ModelSerializer): 

    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OrderPost
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def create(self,validated_data):
        validated_data["owner"]=self.context["request"].user
        order_post=OrderPost.objects.create(**validated_data)
        return order_post





class UserSerializer(serializers.ModelSerializer):
    
    captain = CaptainSerializer(required=False)
    password=serializers.CharField(write_only=True)
    confirm_password=serializers.CharField(write_only=True)
    image = Base64ImageField(required=False)
    orders = OrderPostSerializer(many=True, read_only=True)
    password_updated_message=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields=('id','email','username','created_at','updated_at',
                'first_name', 'last_name', 'password', 'confirm_password',"password_updated_message",
                'is_captain', 'is_client', "governate", "city", "phone_number",'captain',"image","orders")
        read_only_fields=("created_at","updated_at")
    
    #function for insertinf filed message to insure that password was updated
    def get_password_updated_message(self, obj):
        if not self.validated_data.get("password", None) or not self.validated_data.get("confirm_password", None):
             return ("password not updated")
        elif  self.validated_data.get("password") == self.validated_data.get("confirm_password"):
            return ("password updated successfully")
        else:
            return ("password and confirm update didnot match")
        



    @transaction.atomic
    def create(self,validated_data):
        #validation
        #didnot pass password
        if not validated_data.get("password", None) or not validated_data.get("confirm_password", None):
            raise serializers.ValidationError("Please enter a password and "
                                              "confirm it.")
        #didnotmatch
        if validated_data.get("password") != validated_data.get("confirm_password"):
            raise serializers.ValidationError("Those passwords don't match.")
        if validated_data.get("is_client") == validated_data.get("is_captain"):
            raise serializers.ValidationError(
                "you must specify either captain or client ")


        confirm_password = validated_data.pop("confirm_password", None)  # might use it later
        captain_confirm = validated_data.pop("captain", None)
        if validated_data.get("is_client"):
            return User.objects.create_user(**validated_data)
        elif validated_data.get("is_captain"):
                user = User.objects.create_user(**validated_data)
                if captain_confirm:
                    captain= Captain.objects.create(user=user,**captain_confirm)
                    return user
        
    @transaction.atomic
    def update(self,instance,validated_data):
        password=validated_data.pop("password",None)
        confirm_password=validated_data.pop("confirm_password",None)
        captain_data=validated_data.pop("captain",None)
        if instance.is_client:
            instance=super().update(instance, validated_data)
            #sure is captain is false
            instance.is_captain=False
            instance.save()

        elif instance.is_captain:
            instance = super().update(instance, validated_data)
            captain=instance.captain
            #this if cuz we might give captain data with out suppling captain filed
            if captain_data:
                captain.national_id=captain_data.get("national_id",captain.national_id)
                captain.feedback=captain_data.get("feedback",captain.feedback)
                captain.save()
            #sure is_client is false
            instance.is_client = False
            instance.save()

        #updating_password_if_these_conditions_only
        if password and confirm_password and password==confirm_password:
            
            instance.set_password(password)
            instance.save()
            update_session_auth_hash(self.context['request'], instance)
            
                
 
        return instance



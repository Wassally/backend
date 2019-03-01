from rest_framework import serializers
from accounts.models import User,Captain
from django.contrib.auth import update_session_auth_hash

class CaptainSerializer(serializers.ModelSerializer):
    feedback =serializers.CharField(required=False)
    national_id = serializers.IntegerField(required=False)
    
    class Meta:
        model=Captain
        fields=('national_id','feedback')

class UserSerializer(serializers.ModelSerializer):
    
    captain = CaptainSerializer(required=False)
    password=serializers.CharField(write_only=True,required=False)
    confirm_password=serializers.CharField(write_only=True,required=False)
    email=serializers.EmailField(required=True)


    class Meta:
        model=User
        fields=('id','email','username','created_at','updated_at',
                'first_name','last_name','password','confirm_password',
                'is_captain', 'is_client', "governate", "city", "phone_number",'captain')
        read_only_fields=("created_at","updated_at")

    def create(self,validated_data):
        #validation
        #didnot pass password     
        if not validated_data.get("password",None) or not validated_data.get("confirm_password",None):
            raise serializers.ValidationError("Those passwords don't match.")

        #didnotmatch
        if validated_data.get("password") != validated_data.get("confirm_password"):
            raise serializers.ValidationError("Please enter a password and "
                                                                "confirm it.")
        #sure to be client or captain
        confirm_password = validated_data.pop("confirm_password", None)  # might use it later
        captain_confirm = validated_data.pop("captain", None)
        if validated_data.get("is_client"):
            return User.objects.create(**validated_data)
        elif validated_data.get("is_captain"):
            user = User.objects.create(**validated_data)
            if captain_confirm:
                captain= Captain.objects.create(user=user,**captain_confirm)
                return captain
        

    def update(self,instance,validated_data):
        password=validated_data.pop("password",None)
        confirm_password=validated_data.pop("confirm_password",None)
        captain_data=validated_data.pop("captain",None)
        if validated_data.get("is_client"):
            super().update(instance, validated_data)

        elif validated_data.get("is_captain"):
            user = super().update(instance, validated_data)
            captain=user.captain
            captain.national_id=captain_data.get("national_id",captain.national_id)
            captain.feedback=captain_data.get("feedback",captain.feedback)
            captain.save()

        #updating_password_if_these_conditions_only
        if password and confirm_password and password==confirm_password:
            
            user.set_password(password)
            user.save()
            
 
        
        return user



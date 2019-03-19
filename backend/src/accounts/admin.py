from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Captain, Package, Delivery ,Offer,FeedBack

admin.site.register(User)
admin.site.register(Captain)
admin.site.register(Package)
admin.site.register(Delivery)
admin.site.register(Offer)
admin.site.register(FeedBack)




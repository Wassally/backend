from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Captain, OrderPOSt, Delivery ,Offer

admin.site.register(User)
admin.site.register(Captain)
admin.site.register(OrderPOSt)
admin.site.register(Delivery)
admin.site.register(Offer)




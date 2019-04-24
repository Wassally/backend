from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Captain, Package, Delivery, Offer, FeedBack
from django.contrib.gis.admin import OSMGeoAdmin

admin.site.register(User)
admin.site.register(Captain)
admin.site.register(Delivery)
admin.site.register(Offer)
admin.site.register(FeedBack)


@admin.register(Package)
class PackageAdmin(OSMGeoAdmin):
    list_display = ('from_location',)

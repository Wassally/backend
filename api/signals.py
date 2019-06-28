from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import PackageAddress, Package, Address
from api.utils import computing_salary


@receiver(post_save, sender=PackageAddress)
def saving_salary(sender, instance, **kwargs):
    ''' receiver function for saving salary '''
    to_location = instance.to_address.location
    from_location = instance.from_address.location
    to_formated_address = instance.to_address.formated_address
    from_formated_address = instance.from_address.formated_address
    weight = instance.package.weight
    instance.package.wassally_salary = computing_salary(to_formated_address,
                                                        from_formated_address,
                                                        to_location,
                                                        from_location,
                                                        weight)
    instance.package.save()


@receiver(post_save, sender=Address)
def updating_salary(sender, instance, **kwargs):
    update_fields = kwargs["update_fields"]
    if update_fields:
        location = instance.location
        formated_address = instance.formated_address
        if PackageAddress.objects.filter(to_address=instance).exists():
            to_location = location
            to_formated_address = formated_address
            from_location = instance.toaddress.from_address.location
            from_formated_address = \
                instance.toaddress.from_address.formated_address
            package = instance.toaddress.package
            package.wassally_salary = computing_salary(to_formated_address,
                                                       from_formated_address,
                                                       to_location,
                                                       from_location,
                                                       package.weight)
            print(from_location)
            package.save()

        elif PackageAddress.objects.filter(from_address=instance).exists():
            from_location = location
            from_formated_address = formated_address
            to_location = instance.fromaddress.to_address.location
            to_formated_address = \
                instance.fromaddress.to_address.formated_address
            package = instance.fromaddress.package
            package.wassally_salary = computing_salary(to_formated_address,
                                                       from_formated_address,
                                                       to_location,
                                                       from_location,
                                                       package.weight)
            package.save()

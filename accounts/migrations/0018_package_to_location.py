# Generated by Django 2.1.7 on 2019-04-24 05:20

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_remove_package_to_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='to_location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]
# Generated by Django 2.1.7 on 2019-06-20 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20190620_2057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientaddress',
            name='rest_address',
        ),
        migrations.AddField(
            model_name='address',
            name='rest_address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

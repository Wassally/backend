# Generated by Django 2.1.7 on 2019-05-10 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_package_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]

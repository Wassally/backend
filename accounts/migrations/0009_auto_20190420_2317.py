# Generated by Django 2.1.7 on 2019-04-20 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20190420_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='offer_money',
        ),
        migrations.AddField(
            model_name='package',
            name='wassally_salary',
            field=models.IntegerField(default=0),
        ),
    ]

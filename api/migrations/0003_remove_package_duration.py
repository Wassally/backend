# Generated by Django 2.1.7 on 2019-05-10 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190503_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='duration',
        ),
    ]

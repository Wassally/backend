# Generated by Django 2.1.7 on 2019-05-14 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20190514_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='sender_phone_number',
            field=models.CharField(default=0, max_length=14),
        ),
    ]

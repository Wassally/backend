# Generated by Django 2.1.7 on 2019-03-05 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_remove_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.IntegerField(blank=True, default=6545),
        ),
    ]
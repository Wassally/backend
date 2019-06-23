# Generated by Django 2.1.7 on 2019-06-21 20:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20190621_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaddress',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_addresses', to=settings.AUTH_USER_MODEL),
        ),
    ]
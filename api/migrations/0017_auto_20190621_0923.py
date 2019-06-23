# Generated by Django 2.1.7 on 2019-06-21 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20190621_0611'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressdescription',
            name='package',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Package'),
        ),
        migrations.AddField(
            model_name='addressdescription',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
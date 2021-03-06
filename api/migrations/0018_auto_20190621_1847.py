# Generated by Django 2.1.7 on 2019-06-21 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20190621_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressdescription',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Package'),
        ),
        migrations.AlterField(
            model_name='addressdescription',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

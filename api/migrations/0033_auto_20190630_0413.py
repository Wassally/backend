# Generated by Django 2.1.7 on 2019-06-30 02:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_auto_20190630_0305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='captain',
            name='image_national_id',
        ),
        migrations.RemoveField(
            model_name='captain',
            name='national_id',
        ),
        migrations.AlterField(
            model_name='delivery',
            name='package',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.Package'),
        ),
    ]
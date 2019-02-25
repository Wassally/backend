# Generated by Django 2.1.7 on 2019-02-25 14:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_offer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderpost',
            name='time',
        ),
        migrations.AddField(
            model_name='orderpost',
            name='time_day',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='orderpost',
            name='time_hours',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(24)]),
        ),
        migrations.AddField(
            model_name='orderpost',
            name='time_minutes',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(60)]),
        ),
    ]

# Generated by Django 2.1.7 on 2019-04-20 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_package_transport_way'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='transport_way',
            field=models.CharField(choices=[('wassally', 'wassally'), ('other', 'other')], default='wassally', max_length=9),
        ),
    ]

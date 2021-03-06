# Generated by Django 2.1.7 on 2019-05-03 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='from_address',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='package',
            name='from_city',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='package',
            name='from_governate',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='package',
            name='receiver_name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='package',
            name='receiver_phone_number',
            field=models.CharField(max_length=14),
        ),
        migrations.AlterField(
            model_name='package',
            name='to_address',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='package',
            name='to_city',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='package',
            name='to_governate',
            field=models.CharField(max_length=40),
        ),
    ]

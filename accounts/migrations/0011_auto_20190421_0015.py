# Generated by Django 2.1.7 on 2019-04-21 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20190420_2357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='default.png', upload_to='personal/%y/%m/'),
        ),
    ]
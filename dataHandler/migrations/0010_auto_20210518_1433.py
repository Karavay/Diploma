# Generated by Django 3.0.7 on 2021-05-18 11:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dataHandler', '0009_auto_20210514_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='photo',
            field=models.TextField(null=True, verbose_name='profile photo'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='received_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 18, 11, 33, 2, 782733, tzinfo=utc), verbose_name='time of receiving data'),
        ),
    ]
# Generated by Django 3.0.7 on 2021-05-13 18:55

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dataHandler', '0006_auto_20210506_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='last_name',
            field=models.CharField(max_length=30, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='received_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 13, 18, 55, 33, 69763, tzinfo=utc), verbose_name='time of receiving data'),
        ),
    ]

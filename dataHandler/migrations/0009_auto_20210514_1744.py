# Generated by Django 3.0.7 on 2021-05-14 14:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dataHandler', '0008_auto_20210514_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='city_id',
            field=models.CharField(max_length=100, null=True, verbose_name='city id'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='city_title',
            field=models.CharField(max_length=100, null=True, verbose_name='city title'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='country_id',
            field=models.CharField(max_length=100, null=True, verbose_name='country id'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='country_title',
            field=models.CharField(max_length=100, null=True, verbose_name='country title'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='home_town',
            field=models.TextField(null=True, verbose_name='home town'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='received_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 14, 14, 44, 0, 707755, tzinfo=utc), verbose_name='time of receiving data'),
        ),
    ]

from django.db import models

from django.utils import timezone


class UserData(models.Model):
    id = models.CharField('id',max_length = 10,primary_key = True)
    first_name = models.CharField('first name',max_length = 100)
    last_name = models.CharField('last name',max_length = 100)
    sex = models.IntegerField('sex')
    status = models.TextField('user status',null = True)
    city_id = models.CharField('city id',max_length = 100,null = True)
    city_title = models.CharField('city title',max_length = 100,null = True)
    bdate = models.CharField('birth date',max_length = 15,null = True)
    about = models.TextField('about',null = True)
    activities = models.TextField('activities',null = True)
    books = models.TextField('books',null = True)
    career = models.TextField('career',null = True)
    connections = models.TextField('connections',null = True)
    contacts = models.TextField('contacts',null = True)
    country_id = models.CharField('country id',max_length = 100,null = True)
    country_title = models.CharField('country title',max_length = 100,null = True)
    domain = models.CharField('domain',max_length = 50)
    education = models.TextField('education',null = True)
    home_town = models.TextField('home town',null = True)
    received_date = models.DateTimeField('time of receiving data',default = timezone.now())

    def __str__(self):
        return self.domain

    class Meta():
        verbose_name = 'единица информации'
        verbose_name_plural = 'полученные данные'

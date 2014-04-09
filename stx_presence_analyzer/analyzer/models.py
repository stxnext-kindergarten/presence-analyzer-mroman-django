from django.db import models
# from django.db import connections
# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=30)
    avatar = models.CharField(max_length=600)
    legacy_id = models.IntegerField(max_length=50)


class PresenceWeekday(models.Model):
    user = models.ForeignKey(
        'analyzer.User', verbose_name='id')
    day = models.DateField('Data')
    start = models.TimeField('Start')
    end = models.TimeField('End')

from django.db import models

# Create your models here.


class User(models.Model):
    first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30)
    avatar = models.CharField(max_length=600)


class PresenceWeekday(models.Model):
    user = models.ForeignKey(
        'analyzer.User', verbose_name='User')
    day = models.DateField('Data')
    start = models.TimeField('Start')
    end = models.TimeField('End')

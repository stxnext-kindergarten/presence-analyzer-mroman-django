from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30)
    avatar = models.CharField(max_length=600)
    legacy_id = models.IntegerField(max_length=50)


class PresenceWeekday(models.Model):
    user = models.ForeignKey(
        'analyzer.User', verbose_name='User')
    day = models.DateField('Data')
    start = models.TimeField('Start')
    end = models.TimeField('End')

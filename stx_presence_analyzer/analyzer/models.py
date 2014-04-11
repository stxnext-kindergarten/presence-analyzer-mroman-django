from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30)
    avatar = models.CharField(max_length=600)
    legacy_id = models.IntegerField(max_length=50)

    # def test1(self):
    #     return '%s has %d user_id' % (self.first_name, self.legacy_id)

    # def test2(self):
    #     return 'Day is %d, start: %d, end: %d' % (self.day, self.start, self.end)

class PresenceWeekday(models.Model):
    user = models.ForeignKey(
        'analyzer.User', verbose_name='User')
    day = models.DateField('Data')
    start = models.TimeField('Start')
    end = models.TimeField('End')

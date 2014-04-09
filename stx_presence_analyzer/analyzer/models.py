from django.db import models
# from django.db import connections
# Create your models here.

# cursor = connections['db.sqlite3'].cursor()

class User(models.Model):
    first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=30)
    avatar = models.CharField(max_length=600)
    legacy_id = models.IntegerField(max_length=50)

    # for user in User
    # def get_users_as_dict(self):
    #     """ Returns dict with users name and id"""
    #     return [{'user_id': self.legacy_id,
    #         'name': u'User {0}'.format(self.first_name),
    #         'avatar': self.avatar}
    #         for user in User.objects.all()]

class PresenceWeekday(models.Model):
    user = models.ForeignKey(
        'analyzer.User', verbose_name='id')
    # weekday = models.CharField(max_length=10)
    day = models.DateField('Data')
    start = models.TimeField('Start')
    end = models.TimeField('End')

    # def __unicode__(self):
    #     return u"Presence for {}".format(self.user.first_name)

    # def get_presence_as_dict(self):
    #     """ Returns dict with users data """
    #     # return [{'user_id': self.user_id, 'name': u'User {0}'.format(self.first_name)}
    #     #     for user in User.objects.raw('SELECT * FROM analyzer_user')]


    #     return [{self.user:[
    #         (
    #             calendar.day_abbr[weekday], utils.mean(intervals)
    #         )
    #         }
    #         for user in PresenceWeekday.objects.filter(user_id=)
    #     ]



    # def get_presencestartend_as_dict(self):





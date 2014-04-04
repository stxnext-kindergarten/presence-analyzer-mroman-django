import sqlite3, sys
import datetime

from django.core.management.base import BaseCommand, CommandError
from analyzer.models import User, PresenceWeekday


class Command(BaseCommand):
    """
    Napisz nowe polecenie django, które będzie wczytywała dane z plików do bazy. 
    Użyj go do zaczytania danych z poprzednich używanych plików (users and presences),  
    następnie zmień widoki api aby serwowały prawdziwe dane z bazy danych zamiast 
    tych wpisanych na sztywno w poprzednim zadaniu.
    """
    # args = '<analyzer analyzer ...>'
    # help = 'Gets data from files and gives it to database'

    option_list = BaseCommand.option_list + (
        make_option('--data_to_db',
            action='store_true',
            help='File data to DB'),
        make_option('--users_to_db',
            action='store_true',
            help='File users to db'),

    def _get_data():
        """
        Extracts presence data from CSV file and groups it by user_id.

        It creates structure like this:
        data = {
            10: {
                datetime.date(2013, 10, 1): {
                    'start': datetime.time(9, 0, 0),
                    'end': datetime.time(17, 30, 0),
                },
                datetime.date(2013, 10, 2): {
                    'start': datetime.time(8, 30, 0),
                    'end': datetime.time(16, 45, 0),
                },
            },  
            11: {
                datetime.date(2013, 10, 1): {
                    'start': datetime.time(9, 0, 0),
                    'end': datetime.time(17, 30, 0),
                },
                datetime.date(2013, 10, 2): {
                    'start': datetime.time(8, 30, 0),
                    'end': datetime.time(16, 45, 0),
                },
            },
        },
        """
        data = {}
        with open(app.config['DATA_CSV'], 'r') as csvfile:
            presence_reader = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(presence_reader):
                if len(row) != 4:
                    # ignore header and footer lines
                    continue

                try:
                    user_id = int(row[0])
                    date = datetime.strptime(row[1], '%Y-%m-%d').date()
                    start = datetime.strptime(row[2], '%H:%M:%S').time()
                    end = datetime.strptime(row[3], '%H:%M:%S').time()
                except (ValueError, TypeError):
                    log.debug('Problem with line %d: ', i, exc_info=True)  

                data.setdefault(user_id, {})[date] = {'start': start, 'end': end}
        return data

    def _get_data_from_xml():
        """
        Parser get data from users.xml file
        Structure:
        [{
                10: {
                'name': user_name,
                'avatar': url+avatar}
        }]
        """
        with open('runtime/data/users.xml', 'r') as xmlfile:
            tree = etree.parse(xmlfile)
            server = tree.find('./server')
            protocol = server.find('./protocol').text
            host = server.find('./host').text
            additional = '://'
            url = protocol+additional+host
            return {
                user.attrib['id']: {
                    'name': user.find('./name').text,
                    'avatar': url+user.find('./avatar').text}
                for user in tree.findall('./users/user')}

    def handle(self, *args, **options):
        if options['data_to_db']:
            for usr, data in _get_data.iteritems():
                PWU = PresenceWeekday.objects.create(user=usr)
                PWU.save()
                for day, hours in data.iteritems():
                    PWD = PresenceWeekday.objects.create(day=day)
                    PWD.save()

                    hours['start'] = start
                    hours['end'] = end
                    PWH1 = PresenceWeekday.objects.create(start=start)
                    PWH2 = PresenceWeekday.objects.create(end=end)
        if options['users_to_db']:
            for usr, data in _get_data.iteritems():
                PWU = User.objects.create(user=usr)
                PWU.save()
                
                data['avatar'] = avatar
                data['name'] = name
                
                PWA = User.objects.create(avatar=avatar)
                PWA.save()
                PWN = User.objects.create(first_name=name)
                PWN.save()

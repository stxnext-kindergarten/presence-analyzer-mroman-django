# -*- coding: utf-8 -*-

import csv
import io
import sqlite3
import sys
import datetime
import xml.etree.ElementTree as ET

from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from stx_presence_analyzer.analyzer.models import User, PresenceWeekday


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--users_to_db',
                    action='store_true',
                    help='File users and data to db'),)

    def _get_data(self):
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
        with io.open('runtime/data/sample_data.csv', 'r', encoding='utf-8') as csvfile:
            presence_reader = csv.reader(csvfile, delimiter=',')
            for i, row in enumerate(presence_reader):
                if len(row) != 4:
                    # ignore header and footer lines
                    continue
                try:
                    user_id = int(row[0])
                    date = datetime.datetime.strptime(row[1], '%Y-%m-%d').date()
                    start = datetime.datetime.strptime(row[2], '%H:%M:%S').time()
                    end = datetime.datetime.strptime(row[3], '%H:%M:%S').time()
                except (ValueError, TypeError):
                    log.debug('Problem with line %d: ', i, exc_info=True)

                data.setdefault(user_id, {})[date] = {'start': start, 'end': end}
        return data

    def _get_data_from_xml(self):
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
            tree = ET.parse(xmlfile)
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
        if options['users_to_db']:
            get_data1 = self._get_data_from_xml()
            for usr, data in get_data1.iteritems():
                created, PWN = User.objects.get_or_create(
                    first_name=data['name'],
                    avatar=data['avatar'],
                    legacy_id=usr
                    )
            print "Users done!"

            get_data2 = self._get_data()
            for legacy_id, data in get_data2.iteritems():
                try:
                    user = User.objects.get(legacy_id=legacy_id)
                except:
                    print 'User for legacy_id=%d not found' % legacy_id
                else:
                    for day, hours in data.iteritems():
                        start = hours['start']
                        end = hours['end']

                        created, PWD = PresenceWeekday.objects.get_or_create(
                            user=user,
                            day=day,
                            start=start,
                            end=end)

                    print "User %s done" % str(user)
            print "Data done!"

# -*- coding: utf-8 -*-
"""
Presence analyzer unit tests.
"""
import unittest
import datetime
import json

from django.test import TestCase
from django.test.utils import setup_test_environment
from django.test.client import Client

from stx_presence_analyzer.analyzer import utils
from stx_presence_analyzer.analyzer.models import User, PresenceWeekday


class PresenceViewsTestCase(TestCase):
    """ Test class for presences views """

    fixtures = ['stx_presence_analyzer/analyzer/fixtures.json']

    def setUp(self):
        """ Before each test, set up an environment. """
        setup_test_environment()
        self.client = Client()

    def test_mainpage(self):
        """
        Test main page redirect.
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_api_users(self):
        """
        Test users listing.
        """
        resp = self.client.get('/api/v4/users/')
        json_resp = json.loads(resp.content)
        user_151 = json_resp[0]['user_id']

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'application/json')
        self.assertEqual(user_151, 151)

    def test_presence_data_request(self):
        """
        Test presence by weekday and mean time view
        """
        resp = self.client.get('/api/v2/11')
        data = json.loads(resp.content)

        expected_result = [
            ["Weekday", "Presence (s)"],
            ['Mon', 1636630],
            ['Tue', 1658903],
            ['Wed', 1692431],
            ['Thu', 1463881],
            ['Fri', 1139959],
            ['Sat', 86103],
            ['Sun', 86100]
        ]

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'application/json')
        self.assertEqual(data, expected_result)

    def test_presencestartend_data_request(self):
        """
        Test presencestartend time view
        """
        resp = self.client.get('/api/v3/11')
        data = json.loads(resp.content)

        expected_result = [
            ["Mon", 35525.11235955056, 53914.213483146064],
            ["Tue", 33994.325, 54730.6125],
            ["Wed", 33719.951807228914, 54110.68674698795],
            ["Thu", 34043.941860465115, 51065.813953488374],
            ["Fri", 35283.205882352944, 52047.30882352941],
            ["Sat", 32572.5, 54098.25],
            ["Sun", 17366.0, 46066.0]
        ]

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'application/json')
        self.assertEqual(data, expected_result)

    def test_mean_t_week_view_emp_lst(self):
        """
        Test presence and mean time in weekday view for empty list
        """
        resp = self.client.get('/api/v2/1929')
        data = json.loads(resp.content)
        empty_dict = {}
        self.assertEqual(data, empty_dict)

    def test_st_end_view_emp_lst(self):
        """
        Test presencestartend time view for empty list
        """
        resp = self.client.get('/api/v3/1929')
        data = json.loads(resp.content)
        empty_dict = {}
        self.assertEqual(data, empty_dict)


class PresenceAnalyzerUtilsTestCase(unittest.TestCase):
    """
    Utility functions tests.
    """
    fixtures = ['stx_presence_analyzer/analyzer/fixtures.json']

    def setUp(self):
        """ Before each test, set up an environment. """
        setup_test_environment()
        self.client = Client()

    def test_group_by_weekly(self):
        """
        Test group_by_weekday function
        """
        empty_items = []
        items = {
            datetime.date(2013, 9, 11): {
                'end': datetime.time(16, 15, 27),
                'start': datetime.time(9, 13, 26)
            },
            datetime.date(2013, 9, 12): {
                'end': datetime.time(16, 41, 25),
                'start': datetime.time(10, 18, 36)
            }}
        result_1 = utils.group_by_weekday(items)
        result_2 = utils.group_by_weekday(empty_items)

        expected_result_1 = {
            0: [],
            1: [],
            2: [25321],
            3: [22969],
            4: [],
            5: [],
            6: [],
        }

        expected_result_2 = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
        }

        self.assertDictEqual(result_1, expected_result_1)
        self.assertDictEqual(result_2, expected_result_2)

    def test_seconds_since_midnight(self):
        """
        Test seconds_since_midnight function
        """
        input_time_format = datetime.datetime(2014, 3, 11, 14, 26, 25, 230847)
        result_time_for_input = utils.seconds_since_midnight(input_time_format)
        self.assertEqual(result_time_for_input, 51985)

    def test_interval(self):
        """
        Test interval function
        """
        t_start = datetime.datetime.now().time()
        t_end = datetime.datetime.now().time()
        input_time_1 = datetime.datetime(2014, 3, 11, 14, 26, 25, 230847)
        input_time_2 = datetime.datetime(2014, 3, 11, 14, 29, 25, 230847)
        result_time_for_input = utils.interval(input_time_1, input_time_2)

        self.assertLessEqual(t_start, t_end)
        self.assertEqual(result_time_for_input, 180)

    def test_mean(self):
        """
        Test mean function
        """
        strange_lst = [3, 4, 5, 6, 7, 8]
        empty_lst = []
        self.assertEqual(0, utils.mean(empty_lst))
        self.assertEqual(utils.mean(strange_lst), 5.5)

if __name__ == '__main__':
    unittest.main()

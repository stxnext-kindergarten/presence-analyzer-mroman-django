import time

from datetime import datetime

from django.utils import simplejson as json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.views.generic.base import TemplateView


class MainPage(TemplateView):
    """
    Renders main page
    """
    def get_template_names(self):
        """Gets templates names"""
        if self.kwargs == {}:
            self.kwargs = {'template_name': u'presenceweekday'}
        template_name = self.kwargs['template_name']
        available_templates = {
            'home': 'presence_weekday.html',
            'presenceweekday': 'presence_weekday.html',
            'meantimeweekday': 'presence_weekday.html',
            'presencestartend': 'presence_weekday.html'
        }

        return available_templates.get(template_name, 'presence_weekday.html')


class JSONResponseMixin(object):
    def render_to_response(self, context):
        """Returns a JSON response containing 'context' as payload"""
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        """Construct an `HttpResponse` object."""
        return HttpResponse(
            content,
            content_type='application/json',
            **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        """Convert the context dictionary into a JSON object"""
        return json.dumps(context)


class Presence(JSONResponseMixin, TemplateView):
    """
    Class for importing/with data for presence weekday & meantimeweekday
    """
    def get_context_data(self, **kwargs):
        """Get context data method"""
        presences = {
            141: [
                ('Weekday', 'Presence (s)'),
                ('Mon', 383605),
                ('Tue', 370891),
                ('Wed', 356433),
                ('Thu', 356662),
                ('Fri', 319762),
                ('Sat', 45037),
                ('Sun', 0)
                ],
            176: [
                ('Weekday', 'Presence (s)'),
                ('Mon', 0),
                ('Tue', 36331),
                ('Wed', 30575),
                ('Thu', 29815),
                ('Fri', 1),
                ('Sat', 0),
                ('Sun', 0)
                ],
            }
        user_id = int(kwargs['user_id'])
        return presences[user_id]


class PresenceStartEnd(JSONResponseMixin, TemplateView):
    """
    Class for importing/with data for presencestartend
    """
    def get_context_data(self, **kwargs):
        """Get context data method"""
        presences = {
            141: [
                ("Mon", 30441.615384615383, 59949.692307692305),
                ("Tue", 28239.30769230769, 56769.38461538462),
                ("Wed", 29774.75, 59477.5),
                ("Thu", 28521.083333333332, 58242.916666666664),
                ("Fri", 28690.727272727272, 57760.0),
                ("Sat", 28251.0, 73288.0),
                ("Sun", 0, 0)
                ],
            176: [
                ("Mon", 0, 0),
                ("Tue", 32632.0, 50797.5),
                ("Wed", 29643.0, 60218.0),
                ("Thu", 32009.0, 46916.5),
                ("Fri", 32319.0, 32320.0),
                ("Sat", 0, 0),
                ("Sun", 0, 0)
                ],
            }
        user_id = int(kwargs['user_id'])
        return presences[user_id]


class Users(JSONResponseMixin, TemplateView):
    """
    Class for importing/with users names and avatars
    """
    def get_context_data(self, **kwargs):
        """Get context data method"""
        return [
            {'avatar': 'https://intranet.stxnext.pl/api/images/users/141',
                'name': 'Adam P.',
                'user_id': '141'},
            {'avatar': 'https://intranet.stxnext.pl/api/images/users/176',
                'name': 'Adrian K.',
                'user_id': '176'},
            ]

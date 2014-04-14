# -*- coding: utf-8 -*-
import calendar
import logging
import json

from django.http import HttpResponse
from django.views.generic.base import TemplateView

from stx_presence_analyzer.analyzer.models import User, PresenceWeekday
from stx_presence_analyzer.analyzer import utils

logger = logging.getLogger(__name__)


class MainPage(TemplateView):
    """
    Renders main page
    """
    template_name = 'presence_weekday.html'

    def get_context_data(self, template_name=None):
        ctx = super(MainPage, self).get_context_data()
        if template_name == 'meantimeweekday':
            ctx['extra_data'] = {
                'js': 'json_mean_time_weekday.js',
                'title': 'Presence mean time',
            }
        elif template_name == 'presencestartend':
            ctx['extra_data'] = {
                'js': 'json_presence_start_end.js',
                'title': 'Presence start-end',
            }
        else:
            ctx['extra_data'] = {
                'js': 'json_presence_weekday.js',
                'title': 'Presence by weekday',
                }
        return ctx


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

    def _get_data(self):
        """ Get data from model PresenceWeekday and return it"""
        user_id_ok = self.kwargs['user_id']
        data = PresenceWeekday.objects.filter(user__legacy_id=user_id_ok)
        if not data:
            logger.debug('User %s not found!', user_id_ok)
            return {}

        data_presence_dict = {
            presence.day:
                {
                    'start': presence.start,
                    'end': presence.end
                } for presence in data}

        return data_presence_dict


class Presence(JSONResponseMixin, TemplateView):
    """
    Class for importing/with data for presence weekday & meantimeweekday
    """
    def get_context_data(self, **kwargs):
        """Get context data method"""
        data_dict = self._get_data()
        if not data_dict:
            return {}
        weekdays = utils.group_by_weekday(data_dict)

        presences = [
            (
                calendar.day_abbr[weekday], sum(intervals)
            )
            for weekday, intervals in weekdays.items()
        ]
        presences.insert(0, ('Weekday', 'Presence (s)'))
        return presences


class PresenceStartEnd(JSONResponseMixin, TemplateView):
    """
    Class for importing/with data for presencestartend
    """
    def get_context_data(self, **kwargs):
        """Get context data method"""
        data_dict = self._get_data()
        if not data_dict:
            return {}
        weekdays = utils.group_times_by_weekday(data_dict)
        return [
            (
                calendar.day_abbr[weekday],
                utils.mean(times['start']),
                utils.mean(times['end']),
            )
            for weekday, times in weekdays.items()
        ]


class Users(JSONResponseMixin, TemplateView):
    """
    Class for importing/with users names and avatars
    """
    def get_context_data(self, **kwargs):
        """Get context data method"""
        users = User.objects.all()
        return [
            {
                'avatar': user.avatar,
                'name': user.first_name,
                'user_id': user.legacy_id
            }
            for user in users
        ]

from django.conf.urls import patterns, url
from django.contrib import admin

from analyzer.views import MainPage, Presence, PresenceStartEnd, Users


admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$',
        MainPage.as_view(), name='presence_weekday_home'),
    url(r'^(?P<template_name>\w+)/$',
        MainPage.as_view(), name='presence_weekday'),
    url(r'^api/v2/(?P<user_id>\d+)$',
        Presence.as_view(), name='presence'),
    url(r'^api/v3/(?P<user_id>\d+)$',
        PresenceStartEnd.as_view(), name='presence'),
    url(r'^api/v4/users/$',
        Users.as_view(), name='users'),
)

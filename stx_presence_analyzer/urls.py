from django.conf.urls import patterns, url
from django.contrib import admin

from analyzer.views import MainPage, Presence, PresenceStartEnd, Users


admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', MainPage.as_view(), name='presence_weekday_home'),
    url(r'^(?P<template_name>\w+)/$', MainPage.as_view(), name='presence_weekday'),
    url(r'^api/v2/(?P<user_id>\d+)$', Presence.as_view(), name='presence'),
    url(r'^api/v3/(?P<user_id>\d+)$', PresenceStartEnd.as_view(), name='presence'),
    url(r'^api/v4/users/$', Users.as_view(), name='users'),
    #url(r'^api/v2/presence_weekday/<int:user_id>$', Presence.as_view(), name='presence'),
    # url(r'^api/v3/$', SFH_Get_Region_View.as_view(), name='presence'),

    # url(r'normal/api(?P<json_flag>/json/?)$'),
    # Example:

    # (r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

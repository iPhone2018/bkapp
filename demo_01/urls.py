# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns(
    'demo_01.views',
    (r'^get_host_list/$', 'get_host_list'),
    (r'^get_host_by_ip/$', 'get_host_by_ip'),
    (r'^get_biz_all/$', 'get_biz_all'),
    (r'^get_host_all/$', 'get_host_all'),
    (r'^add_host/$', 'add_host'),
    (r'^del_host/$', 'del_host'),
    (r'^edit_host/$', 'edit_host'),

    (r'^resource/(?P<biz_id>[0-9]+)/(?P<host_id>[0-9]+)/$', 'resource')
)
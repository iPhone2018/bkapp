# -*- coding: utf-8 -*-

from django.http import HttpResponse

from common.mymako import render_mako_context, render_json

from blueking.component.shortcuts import get_client_by_request

from demo_01.models import Host


def get_host_list(request):
    hosts = Host.objects.all()
    host_list = []
    for host in hosts:
        _temp = {
            'ip': host.ip,
            'name': host.name,
            'biz': host.biz,
            'cloud_area': host.cloud_area,
            'type': host.type,
            'mark': host.mark
        }
        host_list.append(_temp)
    return render_mako_context(request, '/demo_01/index.html/', {'host_list': host_list})


def get_host_by_ip(request):
    ip = request.POST.get('ip')
    datas = Host.objects.filter(ip=ip).all()
    if not datas:
        return render_json({'data': [], 'result': True})
    hosts = []
    for data in datas:
        _temp = {
            'ip': data.ip,
            'name': data.name,
            'biz': data.biz,
            'cloud_area': data.cloud_area,
            'type': data.type,
            'mark': data.mark
        }
        hosts.append(_temp)
    return render_json({'data': hosts, 'result': True})


def get_biz_all(request):
    client = get_client_by_request(request)
    kw = {
        'fields': ['bk_biz_id', 'bk_biz_name']
    }
    res = client.cc.search_business(kw)
    if not ['result']:
        return render_json({'message': res['message'], 'result': res['result']})

    return render_json({'data': res['data']['info'], 'result': res['result']})


def get_host_all(request):
    client = get_client_by_request(request)
    kw = {
        'fields': ['bk_biz_name']
    }
    res = client.cc.search_host(kw)
    if not ['result']:
        return render_json({'message': res['message'], 'result': res['result']})

    return render_json({'data': res['data']['info'], 'result': res['result']})
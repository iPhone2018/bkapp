# -*- coding: utf-8 -*-
from __future__ import division
import base64
import time

from django.http import HttpResponse

from common.mymako import render_mako_context, render_json

from blueking.component.shortcuts import get_client_by_request

from demo_01.models import Host


def get_host_list(request):
    hosts = Host.objects.all()
    host_list = []
    for host in hosts:
        _temp = {
            'id': host.id,
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
            'id': data.id,
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
    if not res['result']:
        return render_json({'message': res['message'], 'result': res['result']})

    return render_json({'data': res['data']['info'], 'result': res['result']})


def get_host_all(request):
    bk_biz_id = request.GET.get('bk_biz_id')
    client = get_client_by_request(request)
    kw = {
        'bk_biz_id': bk_biz_id
    }
    res = client.cc.search_host(kw)
    if not ['result']:
        return render_json({'message': res['message'], 'result': res['result']})
    host_ips = []
    for host in res['data']['info']:
        host_ips.append({'bk_host_innerip': host['host']['bk_host_innerip']})
    return render_json({'data': host_ips, 'result': res['result']})


def add_host(request):
    bk_biz_id = int(request.POST.get('bk_biz_id'))
    host_ip = request.POST.get('host_ip')
    kw = {
        'condition': [
            {
                "bk_obj_id": "biz",
                "fields": ["bk_biz_name"],
                "condition": [
                    {
                        "field": "bk_biz_id",
                        "operator": "$eq",
                        "value": bk_biz_id
                    }
                ]
            },
            {
                "bk_obj_id": "host",
                "condition": [
                    {
                        "field": "bk_host_innerip",
                        "operator": "$eq",
                        "value": host_ip
                    }
                ]
            }
        ]
    }

    client = get_client_by_request(request)
    res = client.cc.search_host(kw)
    if not res['result']:
        return render_json({'message': res['message'], 'result': res['result']})
    if res['data']['count'] != 1:
        return render_json({'message': 'no data', 'result': False})
    is_host = Host.objects.filter(ip=host_ip).first()
    if is_host:
        return render_json({'message': 'The host is exist!', 'result': False})
    # 插入数据(修改JS)
    host = Host()
    data = res['data']['info'][0]
    host.ip = data['host']['bk_host_innerip']
    host.name = data['host']['bk_host_name']
    host.type = data['host']['bk_os_name']
    host.biz = data['biz'][0]['bk_biz_name']
    host.cloud_area = data['host']['bk_cloud_id'][0]['bk_inst_name']
    host.mark = ''
    host.save()
    res_data = dict(id=host.id, ip=host.ip, name=host.name, type=host.type, biz=host.biz, cloud_area=host.cloud_area,
                    mark=host.mark)
    return render_json({'data': res_data, 'result': True})


def del_host(request):
    id = int(request.POST.get('id'))
    host = Host.objects.filter(id=id).first()
    if not host:
        return render_json({'message': 'The host not exist!', 'result': False})
    host.delete()
    return render_json({'data': [], 'result': True})


def edit_host(request):
    bk_biz_name = request.POST.get('bk_biz_name')
    ip = request.POST.get('ip')
    host = Host.objects.filter(ip=ip).filter(biz=bk_biz_name).first()
    if not host:
        return render_json({'message': 'The host is not exist!', 'result': False})
    host.mark = request.POST.get('mark')
    host.save()
    return render_json({'data': [], 'result': True})


def resource(request, biz_id, host_id):
    # mem_content = "free -m"
    # mem_job_id = execute_script(request, biz_id, host_id, mem_content)

    mem_detail = mem_job_log(request, biz_id, 125)

    # disk_content = "df -h"
    # disk_job_id = execute_script(request, biz_id, host_id, disk_content)

    disk_detail = disk_job_log(request, biz_id, 126)

    # s = new_execute_script(request, biz_id)  # 负载

    return render_mako_context(request, '/demo_01/resource.html/')


def execute_script(request, biz_id, host_id, content):
    host_info = Host.objects.filter(id=host_id).first()
    client = get_client_by_request(request)
    kw = {
        'condition': [
            {
                "bk_obj_id": "host",
                "condition": [
                    {
                        "field": "bk_host_innerip",
                        "operator": "$eq",
                        "value": host_info.ip
                    }
                ]
            }
        ]
    }
    res = client.cc.search_host(kw)

    bk_cloud_id = res['data']['info'][0]['host']['bk_cloud_id'][0]['bk_inst_id']
    script_content = base64.b64encode(content)
    new_kw = {
        'bk_biz_id': int(biz_id),
        'script_content': script_content,
        'account': 'root',
        "ip_list": [
            {
                "bk_cloud_id": bk_cloud_id,
                "ip": host_info.ip
            }
        ]
    }
    new_res = client.job.fast_execute_script(new_kw)
    if not new_res['result']:
        return None
    return new_res['data']['job_instance_id']


def mem_job_log(request, biz_id, mem_job_id):
    time.sleep(2)
    client = get_client_by_request(request)
    kw = {
        'bk_biz_id': int(biz_id),
        'job_instance_id': mem_job_id
    }
    res = client.job.get_job_instance_log(kw)

    if res['data'][0]['status'] == 3:
        log_content = res['data'][0]['step_results'][0]['ip_logs'][0]['log_content']
        log_info = log_content.split('\n')[1].split(':')[1].strip()
        mem_datas = log_info.split('     ')
        total = int(mem_datas[0])
        used = int(mem_datas[1])
        free = int(mem_datas[2])
        cache = int(mem_datas[4])
        used_rate = round((used + cache) / total *100, 2)
        free_rate = round(free / total * 100, 2)
        mem_detail = dict(used_rate=used_rate, free_rate=free_rate)
        return mem_detail
    else:
        return None


def disk_job_log(request, biz_id, disk_job_id):
    time.sleep(2)
    client = get_client_by_request(request)
    kw = {
        'bk_biz_id': int(biz_id),
        'job_instance_id': disk_job_id
    }
    res = client.job.get_job_instance_log(kw)

    if res['data'][0]['status'] == 3:
        disk_detail = []
        log_content = res['data'][0]['step_results'][0]['ip_logs'][0]['log_content'].split('\n')

        for i in log_content[1:]:
            if not i:
                break
            temps = [j for j in i.split(' ') if j]
            _temp = {
                'Filesystem': temps[0],
                'Size': temps[1],
                'Used': temps[2],
                'Avail': temps[3],
                'Userate': temps[4],
                'Mounted': temps[5],
                'On': ''
            }
            disk_detail.append(_temp)
        return disk_detail
    else:
        return None



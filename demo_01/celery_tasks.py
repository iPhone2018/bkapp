# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import base64
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from common.log import logger
from blueking.component.shortcuts import get_client_by_user
from demo_01.models import Host, LoadCondition


@periodic_task(run_every=crontab(minute='*/1', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    execute_task()
    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))


def execute_task():
    now_time = datetime.datetime.now()
    # 查表获取所有ip
    hosts = Host.objects.all()
    if not hosts:
        return None
    client = get_client_by_user(user='admin')
    # 收集所有的ip
    ip_list = []
    for host in hosts:
        kw = {
            'condition': [
                {
                    "bk_obj_id": "host",
                    "condition": [
                        {
                            "field": "bk_host_innerip",
                            "operator": "$eq",
                            "value": host.ip
                        }
                    ]
                }
            ]
        }
        res = client.cc.search_host(kw)

        bk_cloud_id = res['data']['info'][0]['host']['bk_cloud_id'][0]['bk_inst_id']

        ip_list.append({'bk_cloud_id': bk_cloud_id, 'ip': host.ip})

    # 执行脚本
    script_content = base64.b64encode("cat /proc/loadavg")
    new_kw = {
        'bk_biz_id': 2,
        'script_content': script_content,
        'account': 'root',
        "ip_list": ip_list
    }
    new_res = client.job.fast_execute_script(new_kw)
    if not new_res['result']:
        return None

    # 获取内容
    kw_ = {
        'bk_biz_id': 2,
        'job_instance_id': new_res['data']['job_instance_id']
    }
    res_ = client.job.get_job_instance_log(kw_)
    Load_list = list()
    if res_['data'][0]['status'] == 3:
        for ip_log in res_['data'][0]['step_results'][0]['ip_logs']:
            ip = ip_log['ip']
            load_data = ip_log['log_content'].replace("\n", "").split(" ")[1]
            Load_list.append(LoadCondition(ip=ip, load_data=load_data, time=now_time))
        LoadCondition.objects.bulk_create(Load_list)

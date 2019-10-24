# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云(BlueKing) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
"""
import json

from django.http import HttpResponse

from common.mymako import render_mako_context, render_json
from home_application.models import MultRecord


# def index(request):
#     return HttpResponse('Hello')


def home(request):
    """
    首页
    """
    # 获取数据
    mults = MultRecord.objects.all().order_by("-id")
    ctx = {
        'mults': mults
    }
    return render_mako_context(request, '/home_application/home.html', ctx)


def add_datas(request):
    # 获取请求数据
    mult_one = int(request.POST.get('mult_one'))
    mult_two = int(request.POST.get('mult_two'))
    # 计算结果
    result_mut = mult_one * mult_two
    # 存入数据库
    mult_record = MultRecord()
    mult_record.mult_one = mult_one
    mult_record.mult_two = mult_two
    mult_record.mult_result = result_mut
    mult_record.save()

    # 获取数据
    mults = MultRecord.objects.all().order_by("-id")
    datas = []
    for mult in mults:
        datas.append(
            {'id': mult.id, 'mult_one': mult.mult_one, 'mult_two': mult.mult_two, 'mult_result': mult.mult_result})

    return render_json({'result': True, 'result_mut': result_mut, 'mults': datas})


def delete_datas(request):
    id = int(request.POST.get('id'))
    try:
        MultRecord.objects.filter(id=id).delete()
        return render_json({'result': True})
    except:
        return render_json({'result': False})


def update_datas(request):
    id = int(request.POST.get('id'))
    mult_one = int(request.POST.get('mult_one'))
    mult_two = int(request.POST.get('mult_two'))
    mult_result = int(request.POST.get('mult_result'))
    import pdb;pdb.set_trace()

def dev_guide(request):
    """
    开发指引
    """
    return render_mako_context(request, '/home_application/dev_guide.html')


def contactus(request):
    """
    联系我们
    """
    return render_mako_context(request, '/home_application/contact.html')



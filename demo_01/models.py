# -*- coding: utf-8 -*-

from django.db import models


class Host(models.Model):
    # 主机IP
    ip = models.CharField(max_length=100)
    # 主机名称
    name = models.CharField(max_length=255)
    # 所属业务
    biz = models.CharField(max_length=100)
    # 云区域
    cloud_area = models.CharField(max_length=255)
    # 操作系统类型
    type = models.CharField(max_length=100)
    # 备注
    mark = models.CharField(max_length=255)
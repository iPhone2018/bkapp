# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('demo_01', '0002_loadcondition'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loadcondition',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 30, 19, 15, 12, 383000), max_length=255),
        ),
    ]

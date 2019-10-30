# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('demo_01', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoadCondition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=100)),
                ('load_data', models.CharField(max_length=100)),
                ('time', models.CharField(default=datetime.datetime(2019, 10, 30, 16, 38, 48, 63000), max_length=255)),
            ],
        ),
    ]

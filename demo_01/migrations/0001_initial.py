# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
                ('biz', models.CharField(max_length=100)),
                ('cloud_area', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=100)),
                ('mark', models.CharField(max_length=255)),
            ],
        ),
    ]

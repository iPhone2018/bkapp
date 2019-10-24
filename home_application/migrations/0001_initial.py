# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MultRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mult_one', models.IntegerField(verbose_name='\u4e58\u6570')),
                ('mult_two', models.IntegerField(verbose_name='\u88ab\u4e58\u6570')),
                ('mult_result', models.IntegerField(verbose_name='\u7ed3\u679c')),
            ],
        ),
    ]

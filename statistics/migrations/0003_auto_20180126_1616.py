# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-26 16:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0002_auto_20180126_1615'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserInfo',
            new_name='UserInfoForStatistics',
        ),
    ]

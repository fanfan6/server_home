# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-26 16:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='userinfo',
            table='user_info_for_statistics',
        ),
    ]

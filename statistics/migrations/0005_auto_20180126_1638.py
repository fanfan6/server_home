# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-26 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistics', '0004_auto_20180126_1617'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelFeatureRecord',
            fields=[
                ('model_feature_record_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('model_running_record_id', models.BigIntegerField()),
                ('model_feature_id', models.IntegerField()),
                ('created_time', models.BigIntegerField()),
            ],
            options={
                'db_table': 'model_feature_record',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelFeatureVectorRecord',
            fields=[
                ('model_feature_vector_record_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('model_running_record_id', models.BigIntegerField()),
                ('module', models.CharField(max_length=32)),
                ('feature_vector', models.TextField(blank=True, null=True)),
                ('created_time', models.BigIntegerField()),
            ],
            options={
                'db_table': 'model_feature_vector_record',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ModelRunningRecord',
            fields=[
                ('model_running_record_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(blank=True, max_length=32, null=True)),
                ('user_type', models.IntegerField()),
                ('module', models.CharField(max_length=30)),
                ('category', models.IntegerField()),
                ('score', models.FloatField()),
                ('source', models.CharField(max_length=16)),
                ('created_time', models.BigIntegerField()),
            ],
            options={
                'db_table': 'model_running_record',
                'managed': False,
            },
        ),
        migrations.AlterField(
            model_name='userinfoforstatistics',
            name='app_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='userinfoforstatistics',
            name='application_time',
            field=models.CharField(db_index=True, max_length=32, verbose_name='\u7533\u8bf7\u65f6\u95f4'),
        ),
    ]

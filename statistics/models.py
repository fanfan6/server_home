# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class UserInfoForStatistics(models.Model):
    app_id = models.IntegerField(db_index=True)
    name = models.CharField(max_length=64, verbose_name='姓名')
    idcard = models.CharField(max_length=64, verbose_name='身份证号')
    phone = models.CharField(max_length=64, verbose_name='手机号')
    sex = models.CharField(max_length=8, verbose_name='性别')
    native_province = models.CharField(max_length=128, default='', validators='籍贯省')
    native_city = models.CharField(max_length=128, default='', validators='籍贯市')
    native_district = models.CharField(max_length=128, default='', validators='籍贯区')
    native_address = models.CharField(max_length=256, default='', verbose_name='籍贯详细地址')
    education = models.CharField(max_length=256, verbose_name='教育程度')
    jobs = models.CharField(max_length=256, verbose_name='职业')
    live_province = models.CharField(max_length=128, default='', validators='居住地省')
    live_city = models.CharField(max_length=128, default='', validators='居住地市')
    live_district = models.CharField(max_length=128, default='', validators='居住地区')
    live_address = models.CharField(max_length=256, default='', verbose_name='居住地详细地址')
    application_province = models.CharField(max_length=128, default='', validators='申请地省')
    application_city = models.CharField(max_length=128, default='', validators='申请地市')
    application_district = models.CharField(max_length=128, default='', validators='申请地区')
    application_address = models.CharField(max_length=256, default='', verbose_name='申请地详细地址')
    application_time = models.DateTimeField(db_index=True, verbose_name='申请时间')
    create_time = models.DateTimeField(auto_now_add=True)


class ModelFeatureRecord(models.Model):
    model_feature_record_id = models.BigAutoField(primary_key=True)
    model_running_record_id = models.BigIntegerField()
    model_feature_id = models.IntegerField()
    created_time = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'model_feature_record'


class ModelFeatureVectorRecord(models.Model):
    model_feature_vector_record_id = models.BigAutoField(primary_key=True)
    model_running_record_id = models.BigIntegerField()
    module = models.CharField(max_length=32)
    feature_vector = models.TextField(blank=True, null=True)
    created_time = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'model_feature_vector_record'


class ModelRunningRecord(models.Model):
    model_running_record_id = models.BigAutoField(primary_key=True)
    user_id = models.CharField(max_length=32, blank=True, null=True)
    user_type = models.IntegerField()
    module = models.CharField(max_length=30)
    category = models.IntegerField()
    score = models.FloatField()
    source = models.CharField(max_length=16)
    created_time = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'model_running_record'

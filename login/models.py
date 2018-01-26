# coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Pro(models.Model):

    user = models.OneToOneField(User, verbose_name='用户')
    app_id = models.IntegerField(verbose_name='app_id')
    secret = models.CharField(max_length=100, verbose_name='app_id')
    id_num = models.CharField(max_length=100, default='', blank=True, verbose_name='身份证号')
    phone = models.CharField(max_length=200, default='', blank=True, verbose_name="联系电话")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "附加信息"
        ordering = ['-id']

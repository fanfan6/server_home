# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class SearchHistory(models.Model):
    appid = models.IntegerField(db_index=True)
    report_id = models.CharField(max_length=32, blank=True, null=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    phone = models.CharField(max_length=64, blank=True, null=True)
    idcard = models.CharField(max_length=64, blank=True, null=True)
    service = models.CharField(max_length=16)
    search_time = models.CharField(max_length=32)
    create_time = models.IntegerField()

    class Meta:
        db_table = 'search_history'

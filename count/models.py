from __future__ import unicode_literals

from django.db import models

# Create your models here.


class CountClick(models.Model):
    appid = models.IntegerField(db_index=True)
    service = models.CharField(max_length=16, db_index=True)
    clicks = models.CharField(max_length=16)
    date = models.CharField(max_length=32, db_index=True)
    create_time = models.IntegerField()

    class Meta:
        db_table = 'count_click'

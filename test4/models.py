from __future__ import unicode_literals

from django.db import models

# Create your models here.


class test4(models.Model):
    name = models.CharField(max_length=64)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
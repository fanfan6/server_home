# coding=utf-8
from django.shortcuts import render
from statistics import models

import time

# Create your views here.


def index(request):
    app_id = 12345
    # 今日时间的00:00:00转换为时间戳
    yes_time = int(time.time()) - int(time.time()%86400) + time.timezone

    res = models.UserInfoForStatistics.objects.filter(app_id=app_id)
    return render(request, 'static.html', {'res': {}})


def app_pass(request):
    return render(request, 'app_pass.html', {'res':{}})


def mod_grade(request):
    return render(request, 'mod_grade.html', {'res':{}})

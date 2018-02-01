# coding=utf-8
from django.shortcuts import render
from django.utils.timezone import now, timedelta
from statistics import models

import time
import datetime

# Create your views here.


def index(request):
    app_id = 12345
    # 查询的开始时间与结束时间，从当前日期的开始，向前数12个月（包括本月）
    # django ORM 中，使用range按照时间段查询，与Python中range一样，不包括最后一项。因此查询到今天，得到结果相当于查询到昨天
    now_date = time.localtime()
    now_mon = now_date.tm_mon
    now_year = now_date.tm_year - 1
    if int(now_mon) == 12:
        now_mon = 0
        now_year += 1
    start_time = datetime.date(now_year, now_mon + 1, 1)
    end_time = now().date()
    # 查询
    res = models.UserInfoForStatistics.objects.filter(app_id=app_id, application_time__range=(start_time, end_time))
    # 最近12个月的list（年-月）
    if int(end_time.month) == 12:
        all_month = map(lambda x: str(now_year) + '-' + str(x), range(start_time.month, 13))
    else:
        all_month = map(lambda x: str(now_year) + '-' + str(x), range(start_time.month, 13)) + \
                    map(lambda x: str(now_year + 1) + '-' + str(x), range(1, end_time.month + 1))
    res_mon = {}
    print all_month
    for i in all_month:
        select_mon = datetime.date(int(i.split('-')[0]), int(i.split('-')[1]), 1).strftime('%Y-%m')
        res_mon[select_mon] = []
        for j in res:
            if str(j.application_time).startswith(select_mon):
                res_mon[select_mon].append(j)
    print res_mon
    # 过去的12天
    res_day = {}
    for i in range(1, 13):
        select_day = (now().date() + timedelta(days=-i)).strftime('%Y-%m-%d')
        res_day[select_day] = []
        for j in res:
            if str(j.application_time).startswith(select_day):
                res_day[select_day].append(j)

    # 过去的12周
    date_week = []
    # 今天是本周的第几天，从0开始
    now_wday = now_date.tm_wday
    # 本周时间，从周一开始，到昨天
    week11 = []
    for i in range(now_wday + 1):
        week11.append((now().date() + timedelta(days=-i)).strftime('%Y-%m-%d'))
    date_week.append(week11)
    # 其余11周日期
    for each in range(11):
        week12 = []
        for j in range(8):
            week12.append(
                time.strftime('%Y-%m-%d', time.localtime(time.time() - 24 * 60 * 60 * (now_wday + 7 * each + j)))
            )
        date_week.append(week12)
    res_week = []
    for each in date_week:
        start_time = each[-1]
        end_time = each[0]
        res = models.UserInfoForStatistics.objects.filter(app_id=app_id, application_time__range=(start_time, end_time))
        res_week.append(res)

    return render(request, 'static.html', {'res': {}})


def app_pass(request):
    return render(request, 'app_pass.html', {'res':{}})


def mod_grade(request):
    return render(request, 'mod_grade.html', {'res':{}})

# coding=utf-8
from django.shortcuts import render
from django.utils.timezone import now, timedelta
from statistics import models

import time
import datetime

# Create your views here.


def do_count(alist, data):
    # 集合 集齐所有查询过的的data
    a_set = set()
    for each in alist:
        a_set.add(each.get(data))
    # 把查询过的service集合转为list并排序
    data_list = sorted(list(a_set))

    # 新键一个list，用于存放数据。list长度与len(service)相等，以确保每列数据固定，并与data对应
    response = ['0'] * len(data_list)

    for res in alist:
        response[response.index(res.get(data))] += 1

    return data_list, response


class get_date(object):

    def get_all(self):
        # 查询的开始时间与结束时间，从当前日期的开始，向前数12个月（包括本月）
        # django ORM 中，使用range按照时间段查询，与Python中range一样，不包括最后一项。因此查询到今天，得到结果相当于查询到昨天
        self.now_date = time.localtime()
        self.now_mon = self.now_date.tm_mon
        self.now_year = self.now_date.tm_year - 1
        if int(self.now_mon) == 12:
            self.now_mon = 0
            self.now_year += 1
        start_time = datetime.date(self.now_year, self.now_mon + 1, 1)
        end_time = now().date()
        all_date = [start_time, end_time]
        return all_date

    def get_mon(self):
        # 最近12个月的list（年-月）
        if int(self.end_time.month) == 12:
            all_month = map(lambda x: str(self.now_year) + '-' + str(x), range(self.start_time.month, 13))
        else:
            all_month = map(lambda x: str(self.now_year) + '-' + str(x), range(self.start_time.month, 13)) + \
                        map(lambda x: str(self.now_year + 1) + '-' + str(x), range(1, self.end_time.month + 1))
        return all_month

    def get_week(self):
        # 过去的12周
        date_week = []
        # 今天是本周的第几天，从0开始
        now_wday = self.now_date.tm_wday
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
        return date_week

    def get_day(self):
        # 过去的12天
        res_day = []
        for i in range(1, 13):
            select_day = (now().date() + timedelta(days=-i)).strftime('%Y-%m-%d')
            res_day.append(select_day)
        return res_day


def index(request):
    app_id = 12345
    # 查询的开始时间与结束时间，从当前日期的开始，向前数12个月（包括本月）
    # django ORM 中，使用range按照时间段查询，与Python中range一样，不包括最后一项。因此查询到今天，得到结果相当于查询到昨天
    # 查询
    data = get_date()
    all_date = data.get_all()
    start_time = all_date[0]
    end_time = all_date[1]
    res = models.UserInfoForStatistics.objects.filter(app_id=app_id, application_time__range=(start_time, end_time))
    # 查询过去的12个月
    over_12month = data.get_mon()
    res_mon = {}
    for i in over_12month:
        select_mon = datetime.date(int(i.split('-')[0]), int(i.split('-')[1]), 1).strftime('%Y-%m')
        res_mon[select_mon] = []
        for j in res:
            if str(j.application_time).startswith(select_mon):
                res_mon[select_mon].append(j)
    # 过去的12天
    over_12d = data.get_day()
    res_day = {}
    for i in over_12d:
        res_day[i] = []
        for j in res:
            if str(j.application_time).startswith(i):
                res_day[i].append(j)

    # 过去的12周
    date_week = data.get_week()
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

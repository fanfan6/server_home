# coding=utf-8
from django.shortcuts import render
from django.utils.timezone import now, timedelta
from statistics import models
from django.db.models import Q

import time
import numpy
import datetime

# Create your views here.


# 返回需要查询的过去12时， 12日，12周，12月的时间list
class get_date(object):

    def get_mon(self):
        # 查询的开始时间与结束时间，从当前日期的开始，向前数12个月（包括本月）
        # django ORM 中，使用range按照时间段查询，与Python中range一样，不包括最后一项。因此查询到今天，得到结果相当于查询到昨天
        self.now_date = time.localtime()
        self.now_mon = self.now_date.tm_mon
        self.now_year = self.now_date.tm_year - 1
        if int(self.now_mon) == 12:
            self.now_mon = 0
            self.now_year += 1
        self.start_time = datetime.date(self.now_year, self.now_mon + 1, 1)
        self.end_time = now().date()

        # 最近12个月的list（年-月）
        if int(self.end_time.month) == 12:
            all_month = map(lambda x: str(self.now_year) + '-' + str(x) + '-1', range(self.start_time.month, 13))
        else:
            all_month = map(lambda x: str(self.now_year) + '-' + str(x) + '-1', range(self.start_time.month, 13)) + \
                        map(lambda x: str(self.now_year + 1) + '-' + str(x) + '-1', range(1, self.end_time.month + 1))
        return all_month[::-1]

    def get_week(self):
        # 过去的12周
        date_week = []
        # 今天是本周的第几天，从0开始
        now_wday = time.localtime().tm_wday
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

    def get_hour(self):
        res_hour = [int(time.time())]
        for i in range(1, 13):
            res_hour.append(int(time.time()) - 3600 * i)
        return res_hour


# 客户画像
def index(request):
    app_id = 12345
    # 查询的开始时间与结束时间，从当前日期的开始，向前数12个月（包括本月）
    # django ORM 中，使用range按照时间段查询，与Python中range一样，不包括最后一项。因此查询到今天，得到结果相当于查询到昨天
    # 查询
    data = get_date()
    all_date = data.get_mon()
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


# 通过开始时间及结束时间查询，返回申请量，通过量，通过率
def count_number(start_time, end_time):

    all_num = len(models.ModelRunningRecord.objects.filter(created_time__range=(start_time, end_time)))
    pass_num = len(
        models.ModelRunningRecord.objects.filter(
            Q(created_time__range=(start_time, end_time)), Q(category=2) | Q(category=1)
        )
    )
    if int(all_num) == 0:
        res = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)), 0, 0, 0]
    else:
        res = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)), all_num,
               pass_num, round(pass_num/float(all_num), 4)]
    return res


# 申请量，通过量，通过率
def app_pass(request):
    # 过去的12小时
    data = get_date()
    res_hour = []
    for index, j in enumerate(data.get_hour()[:-1]):
        res_hour.append(count_number(data.get_hour()[index + 1], j))

    # 过去的12天
    res_day = []
    for index, each in enumerate(data.get_day()[:-1]):
        day_start_time = int(time.mktime(time.strptime(data.get_day()[index + 1], "%Y-%m-%d")))
        day_end_time = int(time.mktime(time.strptime(each, "%Y-%m-%d")))
        res_day.append(count_number(day_start_time, day_end_time))

    # 过去的12周
    res_week = []
    for w_each in data.get_week():
        week_start_time = int(time.mktime(time.strptime(w_each[-1], "%Y-%m-%d")))
        week_end_time = int(time.mktime(time.strptime(w_each[0], "%Y-%m-%d")))
        res_week.append(count_number(week_start_time, week_end_time))

    # 过去的12个月
    res_mon = []
    for index, each in enumerate(data.get_mon()[:-1]):
        mon_start_time = int(time.mktime(time.strptime(data.get_mon()[index + 1], "%Y-%m-%d")))
        mon_end_time = int(time.mktime(time.strptime(each, "%Y-%m-%d")))
        res_mon.append(count_number(mon_start_time, mon_end_time))
    return render(request, 'app_pass.html', {'res_hour': res_hour, 'res_day': res_day, 'res_week': res_week,'res_mon': res_mon})


def score_content(start_time, end_time):
    data = models.ModelRunningRecord.objects.filter(
        Q(created_time__range=(start_time, end_time)), ~Q(module='simple_zhengxin_policy'),
        ~Q(module='policy'), ~Q(module='finally'), ~Q(module='old_user_model')
    )
    return data, end_time


def not_pass_content(start_time, end_time):
    data = models.ModelRunningRecord.objects.filter(
        Q(created_time__range=(start_time, end_time)), Q(module='simple_zhengxin_policy') |
        Q(module='policy') | Q(module='finally') | Q(module='old_user_model')
    )
    all_num = len(models.ModelRunningRecord.objects.filter(created_time__range=(start_time, end_time)))
    alist = [0] * len(model_feature())
    pro_list = []
    for i in data:
        res = model_feature_record(i.model_running_record_id)
        for i in res:
            alist[i] += 1
    if all_num != 0:
        pro_list = [round(x/float(all_num), 4) for x in alist]
    return alist, pro_list, end_time


def model_feature():
    res = models.ModelFeature.objects.all()
    return res


def model_feature_record(id):
    res = []
    data = models.ModelFeatureRecord.objects.filter(model_running_record_id=id).values('model_feature_id')
    for i in data:
        res.append(i.get('model_feature_id'))
    return res


def do_count(alist):
    # 集合 集齐所有查询过的的data
    a_set = set()
    for eachs in alist:
        for each in eachs:
            a_set.add(each.module)
    # 把查询过的service集合转为list并排序
    data_list = sorted(list(a_set))
    # 新键一个list，用于存放数据。list长度与len(service)相等，以确保每列数据固定，并与data对应
    res = []
    res2 = []
    for eachs in alist:
        a = [0] * len(data_list)
        for each in eachs:
            a[data_list.index(each.module)] = each.score
        res.append(a)
    res1 = map(list, zip(*res))

    for each in res1:
        if not res1:
            res2.append([0, 0, 0, 0, 0, 0, 0, 0])
        else:
            res2.append([numpy.average(each), numpy.min(each), numpy.percentile(each, 5), numpy.percentile(each, 25),
                         numpy.percentile(each, 50), numpy.percentile(each, 75), numpy.percentile(each, 95),
                         numpy.max(each)])
    return [data_list, res2]


# 模型评分
def mod_grade(request):
    data = get_date()
    # 过去的12时
    res_hour = []
    res_hour2 = []
    for index, j in enumerate(data.get_hour()[:-1]):
        res, end_time = score_content(data.get_hour()[index + 1], j)
        alist_hour, pro_list_hour, end_time_hour = not_pass_content(data.get_hour()[index + 1], j)
        res_hour.append([res, end_time])
        res_hour2.append([alist_hour, pro_list_hour, time.strftime("%H:%M:%S", time.localtime(end_time_hour))])
    response_hour = []
    hour_data_list = []
    for i in res_hour:
        res = do_count(i[:-1])
        if res[0]:
            hour_data_list = res[0]
        res.insert(0, time.strftime("%H:%M:%S", time.localtime(i[-1])))
        response_hour.append(res)

    # 过去12天
    res_day = []
    res_day2 = []
    for index, each in enumerate(data.get_day()[:-1]):
        day_start_time = int(time.mktime(time.strptime(data.get_day()[index + 1], "%Y-%m-%d")))
        day_end_time = int(time.mktime(time.strptime(each, "%Y-%m-%d")))
        res, end_time = score_content(day_start_time, day_end_time)
        alist_day, pro_list_day, end_time_day = not_pass_content(day_start_time, day_end_time)
        res_day.append([res, end_time])
        res_day2.append([alist_day, pro_list_day, time.strftime("%Y-%m-%d", time.localtime(end_time_day))])
    response_day = []
    day_data_list = []
    for i in res_day:
        res = do_count(i[:-1])
        if res[0]:
            day_data_list = res[0]
        res.insert(0, time.strftime("%Y-%m-%d", time.localtime(i[-1])))
        response_day.append(res)
    print res_day2
    # 过去的12周
    res_week = []
    for w_each in data.get_week():
        week_start_time = int(time.mktime(time.strptime(w_each[-1], "%Y-%m-%d")))
        week_end_time = int(time.mktime(time.strptime(w_each[0], "%Y-%m-%d")))
        res, end_time = score_content(week_start_time, week_end_time)
        res_week.append([res, end_time])
    response_week = []
    week_data_list = []
    for i in res_week:
        res = do_count(i[:-1])
        if res[0]:
            week_data_list = res[0]
        res.insert(0, time.strftime("%Y-%m-%d", time.localtime(i[-1])))
        response_week.append(res)

    # 过去的12个月
    res_mon = []
    for index, each in enumerate(data.get_mon()[:-1]):
        mon_start_time = int(time.mktime(time.strptime(data.get_mon()[index + 1], "%Y-%m-%d")))
        mon_end_time = int(time.mktime(time.strptime(each, "%Y-%m-%d")))
        res, end_time = score_content(mon_start_time, mon_end_time)
        res_mon.append([res, end_time])
    response_mon = []
    mon_data_list = []
    for i in res_mon:
        res = do_count(i[:-1])
        if res[0]:
            mon_data_list = res[0]
        res.insert(0, time.strftime("%Y-%m-%d", time.localtime(i[-1])))
        response_mon.append(res)

    return render(request, 'mod_grade.html', {'response_hour': response_hour, 'response_day': response_day,
                                              'response_week': response_week, 'response_mon': response_mon,
                                              'mod_h': hour_data_list, 'mod_d': day_data_list, 'mod_w': week_data_list,
                                              'mod_m': mon_data_list, 'res_day2': res_day2})


def conformity(res, content):
    data = date_format()
    for i in res:
        print i

# 时间的表达格式
def date_format():
    hour = []
    day = []
    week = []
    month = []
    data = get_date()
    for i in data.get_hour():
        hour.append(time.strftime("%H:%M", time.localtime(i)))
    for i in data.get_day():
        day.append(i[-5:])
    for i in data.get_week():
        week.append(i[-1][-5:] + '/' + i[0][-5:])
    for i in data.get_mon():
        month.append(i)
    return [hour, day, week, month]




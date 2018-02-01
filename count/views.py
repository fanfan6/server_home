# coding=utf-8
from django.shortcuts import render, HttpResponse
from django.db.models import Q, Count
from django.http import StreamingHttpResponse

# Create your views here.
import datetime
import xlwt
import StringIO
from count import models

TEXT = ''


def counts(request):
    return render(request, 'counts.html', {'res': {}})


def public_info(request):
    try:
        appid = 100256
        start_time = request.GET['start_time'].replace('-', '')
        end_time = request.GET['end_time'].replace('-', '')
        oneday = datetime.timedelta(days=1)
        # 若结束时间比当前时间晚，则把结束时间改为昨天
        if end_time >= datetime.datetime.now().strftime('%Y%m%d'):
            end_time = (datetime.datetime.now() - oneday).strftime('%Y%m%d')
        # 若结束时间早于开始时间，则开始时间与结束时间互换
        if end_time <= start_time:
            start_time, end_time = end_time, start_time
        res = models.CountClick.objects.filter(Q(appid=appid), Q(date__lte=end_time), Q(date__gte=start_time)).values()
        # 集合 集齐所有查询过的的service
        service_set = set()
        for each_service in res:
            service_set.add(each_service.get('service'))
        # 把查询过的service集合转为list并排序
        service = sorted(list(service_set))
        response = []

        # 按照时间遍历
        datestart = datetime.datetime.strptime(start_time, '%Y%m%d')
        dateend = datetime.datetime.strptime(end_time, '%Y%m%d')
        while datestart < dateend:
            num = dateend.strftime('%Y%m%d')
            # 新键一个list，用于存放数据。list长度与len(service)相等，以确保每列数据固定，并与service对应
            service_res = ['0'] * len(service)
            for i in res:
                # 若res中时间字段与当前时间字段对应，
                if i.get('date') == str(num):
                    # 将clicks的值添加到service_res中，下标为‘service’字段在service列表中的下标
                    service_res[service.index(i.get('service'))] = i.get('clicks')
            # 添加其它元素，（末尾添加当前list的总和）
            response.append({'date': str(num)[:4] + '-' + str(num)[4:6] + '-' + str(num)[6:],
                             'service': service_res, 'sum': sum(map(int, service_res))})
            # 时间往前一天
            dateend -= datetime.timedelta(days=1)

        alist = []
        # 把所有数据转换为矩阵
        for i in response:
            alist.append(map(int, i['service']))
        # 使用矩阵知识对每列求和
        service_sum = map(sum, zip(*alist))
        all_sum = sum(service_sum)
        date = {'start_time': start_time[:4] + '-' + start_time[4:6] + '-' + start_time[6:],
                'end_time': end_time[:4] + '-' + end_time[4:6] + '-' + end_time[6:]}

        return {'res': response, 'service': service, 'service_sum': service_sum, 'all_sum': all_sum, 'date': date}
    except:
        return {}


def count_info(request):
    print 'count_info'
    data = public_info(request)
    if data:
        global TEXT
        TEXT = data
        response = data.get('res')
        service = data.get('service')
        service_sum = data.get('service_sum')
        all_sum = data.get('all_sum')
        date = data.get('date')
        return render(request, 'counts.html', {'res': response, 'service': service, 'service_sum': service_sum,
                                               'all_sum': all_sum, 'date': date})
    else:
        return render(request, 'counts.html', {})


def count_download(request):
    print 'count_download'
    global TEXT
    data = TEXT
    if data:
        response = data.get('res')
        service = data.get('service')
        service_sum = data.get('service_sum')
        all_sum = data.get('all_sum')
        if response:
            ws = xlwt.Workbook(encoding='utf-8')
            w = ws.add_sheet(u"数据报表第一页")
            w.write(0, 0, "日期")
            for index, value in enumerate(service):
                w.write(0, index + 1, value)
            w.write(0, len(service) + 1, '总计')
            excel_row = 1
            for i in response:
                w.write(excel_row, 0, i.get('date'))
                for index, j in enumerate(i.get('service')):
                    w.write(excel_row, index + 1, j)
                w.write(excel_row, len(service) + 1, i.get('sum'))
                excel_row += 1
            w.write(excel_row, 0, '总计')
            for index, m in enumerate(service_sum):
                w.write(excel_row, index + 1, m)
            w.write(excel_row, len(service) + 1, all_sum)

            sio = StringIO.StringIO()
            ws.save(sio)
            sio.seek(0)
            response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=报表.xls'
            response.write(sio.getvalue())
            return response
    else:
        return render(request, 'counts.html', {})

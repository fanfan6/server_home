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
        if end_time >= datetime.datetime.now().strftime('%Y%m%d'):
            end_time = (datetime.datetime.now() - oneday).strftime('%Y%m%d')
        if end_time <= start_time:
            start_time, end_time = end_time, start_time
        res = models.CountClick.objects.filter(Q(appid=appid), Q(date__lte=end_time), Q(date__gte=start_time)).values()
        service_set = set()
        for each_service in res:
            service_set.add(each_service.get('service'))
        service = sorted(list(service_set))
        response = []

        # 时间遍历
        datestart = datetime.datetime.strptime(start_time, '%Y%m%d')
        dateend = datetime.datetime.strptime(end_time, '%Y%m%d')

        while datestart < dateend:
            num = dateend.strftime('%Y%m%d')
            service_res = ['0'] * len(service)
            for i in res:
                if i.get('date') == str(num):
                    service_res[service.index(i.get('service'))] = i.get('clicks')
            response.append({'date': str(num)[:4] + '-' + str(num)[4:6] + '-' + str(num)[6:], 'service': service_res, 'sum': sum(map(int, service_res))})
            dateend -= datetime.timedelta(days=1)

        alist = []
        for i in response:
            alist.append(map(int, i['service']))
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

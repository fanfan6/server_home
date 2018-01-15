# coding=utf-8
from django.shortcuts import render

# Create your views here.
import json
import urllib
import urllib2
import collections
import hashlib

from report_info import models

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def report(request, nid):
    user_info = {}
    report_id = nid
    print(report_id)
    report_info = models.ReportRecord.objects.get(report_id=report_id)

    report_type = report_info.report_type
    report_datail = json.loads(report_info.report_datail)

    base_info = report_datail.get('base_info')
    if base_info['gender'] == 0:
        gender = u'女'
    else:
        gender = u'男'

    # 个人信息
    user_info['gender'] = gender
    user_info['age'] = base_info['age']
    user_info['name'] = base_info['name']
    user_info['phone'] = base_info['phone']
    user_info['idcard'] = base_info['idcard']

    credit_report_summary = report_datail.get('credit_report_summary')
    if credit_report_summary[0].get('module') == 'model_score':
        credit_report_summary[0]['module'] = u'模型分(V1)'
    elif credit_report_summary[0].get('module') == 'credit_score':
        credit_report_summary[0]['module'] = u'信用分(V2)'
    try:
        if credit_report_summary[1].get('module') == 'model_score':
            credit_report_summary[1]['module'] = u'模型分(V1)'
        elif credit_report_summary[1].get('module') == 'credit_score':
            credit_report_summary[1]['module'] = u'信用分(V2)'
    except:
        pass
    sub_report = report_datail.get('sub_report')
    simport_zhengxin = {'feature': {}}

    if int(report_type) == 201:
        # 获取报告子模块
        simport_zhengxin_report = sub_report.get('simport_zhengxin_report')
        multi_loan_report = sub_report.get('multi_loan_report')
        zhima_report = sub_report.get('zhima_report')
        asset_report = sub_report.get('asset_report')
        yys_report = sub_report.get('yys_report')

        simport_zhengxin['summary'] = simport_zhengxin_report.get('summary', '')
        simport_zhengxin['rule'] = simport_zhengxin_report.get('rule', '')
        simport_zhengxin['score_quantile'] = simport_zhengxin_report.get('score_quantile', '')

        # 简版征信报告
        # 征信报告是否本人
        if simport_zhengxin_report.get('feature', '').get('simple_zhengxin_inequal_name', ''):
            simport_zhengxin['feature']['simple_zhengxin_inequal_name'] = u'是'
        else:
            simport_zhengxin['feature']['simple_zhengxin_inequal_name'] = u'否'

        # 是否有强制执行记录
        if simport_zhengxin_report.get('feature', '').get('simple_zhengxin_has_compulsory_execution_record', ''):
            simport_zhengxin['feature']['simple_zhengxin_has_compulsory_execution_record'] = u'是'
        else:
            simport_zhengxin['feature']['simple_zhengxin_has_compulsory_execution_record'] = u'否'

        # 信用卡是否出现过呆账/冻结/止付状态
        if simport_zhengxin_report.get('feature', '').get('simple_zhengxin_credit_card_abnormal', ''):
            simport_zhengxin['feature']['simple_zhengxin_credit_card_abnormal'] = u'是'
        else:
            simport_zhengxin['feature']['simple_zhengxin_credit_card_abnormal'] = u'否'

        # 房贷是否出现过呆账/冻结/止付状态
        if simport_zhengxin_report.get('feature', '').get('simple_zhengxin_house_loan_abnormal', ''):
            simport_zhengxin['feature']['simple_zhengxin_house_loan_abnormal'] = u'是'
        else:
            simport_zhengxin['feature']['simple_zhengxin_house_loan_abnormal'] = u'否'

        # 其他贷款是否出现过呆账/冻结/止付状态
        if simport_zhengxin_report.get('feature', '').get('simple_zhengxin_other_loan_abnormal', ''):
            simport_zhengxin['feature']['simple_zhengxin_other_loan_abnormal'] = u'是'
        else:
            simport_zhengxin['feature']['simple_zhengxin_other_loan_abnormal'] = u'否'

        # 人民币信用卡数
        simport_zhengxin['feature']['simple_zhengxin_credit_card_cnt'] = simport_zhengxin_report.get('feature', '').get('simple_zhengxin_credit_card_cnt', '0')
        # 其他贷款笔数
        simport_zhengxin['feature']['simple_zhengxin_other_loan_cnt'] = simport_zhengxin_report.get('feature', '').get('simple_zhengxin_other_loan_cnt', '0')
        # 房贷笔数
        simport_zhengxin['feature']['simple_zhengxin_house_loan_cnt'] = simport_zhengxin_report.get('feature', '').get('simple_zhengxin_house_loan_cnt', '0')
        # 信用卡最早激活时间
        simport_zhengxin['feature']['simple_zhengxin_earliest_credit_card_release_date'] = simport_zhengxin_report.get('feature', '').get('simple_zhengxin_earliest_credit_card_release_date', '0')
        # 当前信用卡逾期卡数
        simport_zhengxin['feature']['simple_zhengxin_current_overdue_credit_card_num'] = simport_zhengxin_report.get('feature', '').get('simple_zhengxin_current_overdue_credit_card_num', '0')
        # 当前信用卡逾期金额
        simport_zhengxin['feature']['simple_zhengxin_credit_card_current_overdue_amount'] = simport_zhengxin_report.get('feature', '').get('simple_zhengxin_credit_card_current_overdue_amount', '0')
        # 近五年信用卡逾期超过90天次数
        simport_zhengxin['feature']['simple_zhengxin_credit_card_overdue_days_exceed_90_times'] = simport_zhengxin_report.get('feature', '').get('simple_zhengxin_credit_card_overdue_days_exceed_90_times', '0')
        # 当前房贷逾期金额
        simport_zhengxin['feature']['simple_zhengxin_house_loan_current_overdue_amount'] = simport_zhengxin_report.get('feature', '').get('simple_zhengxin_house_loan_current_overdue_amount', '0')
        # 近五年房贷逾期超过90天次数
        simport_zhengxin['feature']['simple_zhengxin_house_loan_overdue_days_exceed_90_times'] = simport_zhengxin_report.get('feature', '').get('simple_zhengxin_house_loan_overdue_days_exceed_90_times', '0')
        # 当前其他贷款逾期金额
        simport_zhengxin['feature']['simple_zhengxin_other_loan_current_overdue_amount'] = simport_zhengxin_report.get('feature', '').get('simple_zhengxin_other_loan_current_overdue_amount', '0')
        # 近五年其它贷款逾期超过90天次数
        simport_zhengxin['feature']['simple_zhengxin_other_loan_overdue_days_exceed_90_times'] = simport_zhengxin_report.get('feature', '').get('simple_zhengxin_other_loan_overdue_days_exceed_90_times', '0')

        # 多头借贷报告
        multi_loan = {'feature': multi_loan_report.get('feature', '').get('multi_loan_apply_cnt', '0'),
                      'rule': multi_loan_report.get('rule', '')}

        # 芝麻信用报告
        zhima_info = {'score': zhima_report.get('summary').get('score'),
                      'score_quantile': zhima_report.get('summary').get('score_quantile') * 100,
                      'rule': zhima_report.get('rule', '')}

        # 资产消费报告
        asset_info = {'score': asset_report.get('summary').get('score'),
                      'score_quantile': asset_report.get('summary').get('score_quantile') * 100,
                      'rule': asset_report.get('rule', '')}

        # 运营商报告
        # 姓名与运营商是否匹配
        feature = {}
        if yys_report.get('feature', '').get('yys_inequal_name', ''):
            feature['yys_inequal_name'] = u'否'
        else:
            feature['yys_inequal_name'] = u'是'

        # 入网时间
        feature['yys_reg_time'] = yys_report.get('feature').get('yys_reg_time')
        # 当前账户余额
        feature['cur_account_amount'] = yys_report.get('feature').get('cur_account_amount')
        # 最近180天最长静默时间（天）
        feature['longest_no_call_time'] = yys_report.get('feature').get('longest_no_call_time')
        # 最近180天通话次数
        feature['total_cnt_l180d'] = yys_report.get('feature').get('total_cnt_l180d')
        # 最近180天通话时长（秒）
        feature['total_duration_l180d'] = yys_report.get('feature').get('total_duration_l180d')
        # 最近180天主叫次数
        feature['total_call_cnt_l180d'] = yys_report.get('feature').get('total_call_cnt_l180d')
        # 最近180天主叫时长（秒）
        feature['total_call_duration_l180d'] = yys_report.get('feature').get('total_call_duration_l180d')
        # 最近180天夜间通话次数
        feature['total_night_cnt_l180d'] = yys_report.get('feature').get('total_night_cnt_l180d')
        # 最近180天夜间通话时长（秒）
        feature['total_night_duration_l180d'] = yys_report.get('feature').get('total_night_duration_l180d')
        # 最近180天通话号码数（去重）
        feature['total_phone_no_cnt_l180d'] = yys_report.get('feature').get('total_phone_no_cnt_l180d')
        # 最近180天通话次数超过10次的号码占比
        feature['cnt_more_than_10_ratio_l180d'] = yys_report.get('feature').get('cnt_more_than_10_ratio_l180d')
        # 最近180天与贷款类号码通话次数
        feature['telephone_call_phone_lable_loan_cnt'] = yys_report.get('feature').get('telephone_call_phone_lable_loan_cnt')
        # 最近180天与催收类号码通话次数
        feature['telephone_call_phone_lable_cuishou_cnt'] = yys_report.get('feature').get('telephone_call_phone_lable_cuishou_cnt')

        yys_info = {'score': yys_report.get('summary').get('score'),
                    'score_quantile': yys_report.get('summary').get('score_quantile') * 100,
                    'feature': feature,
                    'rule': yys_report.get('rule', '')}

        return render(request, 'userinfo2.html', {'user_info': user_info, 'simport_zhengxin': simport_zhengxin, 'multi_loan': multi_loan,
                                                  'report_type': report_type, 'credit_report_summary': credit_report_summary,
                                                  'zhima_info': zhima_info, 'asset_info': asset_info, 'yys_info': yys_info})
    elif int(report_type) == 202:
        sub_info = {
            'behavior_level_1': base_info.get('behavior_level_1', ''),
            'behavior_level_2': base_info.get('behavior_level_2', ''),
            'behavior_level_3': base_info.get('behavior_level_3', ''),
            'social_level_1': base_info.get('social_level_1', ''),
            'social_level_2': base_info.get('social_level_2', ''),
            'social_level_3': base_info.get('social_level_3', ''),
            'stable_level_1': base_info.get('stable_level_1', ''),
            'stable_level_2': base_info.get('stable_level_2', ''),
            'stable_level_3': base_info.get('stable_level_3', ''),
            'fraud_level_1': base_info.get('fraud_level_1', ''),
            'fraud_level_2': base_info.get('fraud_level_2', ''),
            'fraud_level_3': base_info.get('fraud_level_3', ''),
            'performance_level_1': base_info.get('performance_level_1', ''),
            'performance_level_2': base_info.get('performance_level_2', ''),
            'performance_level_3': base_info.get('performance_level_3', ''),
        }
        return render(request, 'userinfo1.html', {'user_info': user_info, 'credit_report_summary': credit_report_summary, 'sub_info': sub_info})


def post(req_url, req_data, timeout=10):
    if isinstance(req_data, dict):
        req_data = urllib.urlencode(req_data)
    request = urllib2.Request(url=req_url, data=req_data)
    return urllib2.urlopen(request, timeout=timeout)


def __params_encode(params, secret):
    ordered_params = collections.OrderedDict(sorted(params.items(), key=lambda t: t[0]))
    items = []
    for key in ordered_params.keys():
        items.append(key + '=' + str(ordered_params[key]))
    items.append(secret)
    params_str = '&'.join(items)
    print params_str
    return hashlib.md5(params_str.encode('utf-8')).hexdigest()


def add_sign(params, secret):
    sign = __params_encode(params, secret)
    params['sign'] = sign
    return params


def search(request):
    print('search')
    return render(request, 'search.html')


def search_info(request):
    print('search_info')
    request.encoding = 'utf-8'
    name = request.GET['name']
    idcard = request.GET['idcard']
    phone = request.GET['phone']
    service = request.GET['service']
    data = {
        'appid': 100256,
        'idcard': '331082199401231014',
        'name': '李灵杰',
        'phone': '13105866570',
        'service': 'S06'
    }
    # add_sign(data, 'a1a8fd0bef522844')
    # res = post('http://10.141.148.247/api/get_data', data).read()
    # print(res)
    res = {"message": "\u67e5\u8be2\u6210\u529f",
           "code": "R0000",
           "data":
               {"credit_score": 660,
                "sub_features":
                    {"behavior_level_1": 0.0476,
                     "behavior_level_2": 0.2381,
                     "behavior_level_3": 0.4286,
                     "social_level_1": 90.0,
                     "social_level_3": 90.0,
                     "stable_level_1": 1.2111,
                     "stable_level_3": 48.0,
                     "stable_level_2": 23.0651,
                     "social_level_2": 0.0,
                     "fraud_level_3": 93.75,
                     "fraud_level_2": 1030.0,
                     "fraud_level_1": 515.0,
                     "performance_level_3": 150.4545,
                     "performance_level_2": 28.0,
                     "performance_level_1": 135.7828
                     },
                "is_black": 1,
                "model_score": 656
                }
           }
    response = {}
    if res['data']['is_black'] == 1:
        response['is_black'] = u'是'
    elif res['data']['is_black'] == 0:
        response['is_black'] = u'否'
    response['model_score'] = res['data']['model_score']
    response['credit_score'] = res['data']['credit_score']
    response['sub_features'] = res['data']['sub_features']
    response['report_id'] = '100273151599925189875'

    return render(request, 'search.html', {'res': response})


def service(request):
    return render(request, 'service.html')

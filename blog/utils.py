# -*- coding: utf-8 -*-

import json
import urllib2


'''
使用正则表达式元组查找是否包含mobile、iphone、android、iemobile
为避免每次都要查询，将第一次的结构保存到session中，
session中有记录就直接返回session中的结果，不在继续判断
'''
import re
user_device_re = re.compile(r'(mobile|iphone|android|iemobile)')

def get_user_device(request):
    # return 'MOBILE'
    device = request.session.get('USER_VIEW_DEVICE','UNKNOWN_VIEW_DEVICE')
    if device != 'UNKNOWN_VIEW_DEVICE':
        return device

    HTTP_USER_AGENT = request.META.get('HTTP_USER_AGENT', '').lower()
    print HTTP_USER_AGENT
    user_device = user_device_re.findall(HTTP_USER_AGENT)
    if len(user_device) > 0:
        request.session['USER_VIEW_DEVICE'] = 'MOBILE'
        return 'MOBILE'

    request.session['USER_VIEW_DEVICE'] = 'PC'
    return 'PC'

# def get_user_device(request):
#
#     # return 'MOBILE'
#     HTTP_USER_AGENT = request.META.get('HTTP_USER_AGENT', '').lower()
#     user_device_re = r'(mobile|iphone|android|iemobile)'
#     print '*****HTTP_USER_AGENT:*****',HTTP_USER_AGENT
#     device = request.session.get('USER_VIEW_DEVICE','UNKNOWN_VIEW_DEVICE')
#     if device != 'UNKNOWN_VIEW_DEVICE':
#         if device == 'MOBILE':
#             return device
#         else:
#             return 'PC'
#     HTTP_USER_AGENT = request.META.get('HTTP_USER_AGENT', '').lower()
#     print '*****HTTP_USER_AGENT:*****',HTTP_USER_AGENT
#     for device in ['iphone', 'android', 'iemobile',]:
#         if device in HTTP_USER_AGENT:
#             request.session['USER_VIEW_DEVICE'] = 'MOBILE'
#             return 'MOBILE'
#     request.session['USER_VIEW_DEVICE'] = 'PC'
#     return 'PC'

def get_user_ip(request):
    return request.META.get('REMOTE_ADDR','0.0.0.0')

def get_ip_location(ip):
    if ip == '0.0.0.0':
        return ''
    try :
        url = 'http://ip.taobao.com/service/getIpInfo.php?ip=%s' % ip
        location = urllib2.urlopen(url).read()
        location = json.loads(location)
        location = location['data']
        address  = ''
        if location['country'] != '':
            address += location['country'] + ' '
        if location['region'] != '':
            address += location['region'] + ' '
        if location['area'] != '':
            address += location['area'] + ''
        if location['isp'] != '':
            address += location['isp']
        return address
    except :
        return ''
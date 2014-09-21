#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse,Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from blog.utils import get_user_device, get_user_ip
from models import BingWallPaper
import re
import os.path
import time
import datetime
import StringIO
import urllib2
import uuid
import qiniu.conf
import qiniu.io
import qiniu.rs

qiniu.conf.ACCESS_KEY = "<YOUR_APP_ACCESS_KEY>"
qiniu.conf.SECRET_KEY = "<YOUR_APP_SECRET_KEY>"
QINIU_BUCKET_NAME = '<YOUR_BUCKET_NAME>'

policy = qiniu.rs.PutPolicy(QINIU_BUCKET_NAME)
uptoken = policy.token()

# def save_img(img_url):
#     try:
#         img_name = img_url[img_url.rindex('/')+1:]
#         img_data = urllib2.urlopen(img_url).read()
#         img_fuffix = img_name[img_name.rindex('.'):]

#         todaytime = datetime.datetime.now().strftime('%Y%m%d')

#         name = os.path.join('bing',uuid.uuid1().hex + img_fuffix).replace('\\','/')
#         ret, err = qiniu.io.put(uptoken, name, img_data)
#         if err is not None:
#             print err
#             return 'error',todaytime,'',''
#         url = 'http://'+QINIU_BUCKET_NAME+'.qiniudn.com/'+name
#         return 'success',todaytime,img_name,url
#     except:
#         return 'error',todaytime,'',''


# def savebing(request):
#     url = 'http://cn.bing.com'
#     try:
#         html = urllib2.urlopen(url).read()
#         img_url = re.findall(r"g_img={url:'(.+?)'",html)[0]
#         print save_img(img_url)
#     except:
#         print 'failed'
#     # num = 1
#     # tn = time.time()
#     # url = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=%d&n=1&nc=%d&pid=hp&scope=web&FORM=QBRE&video=1'%(num,int(tn))
#     # response = urllib2.urlopen(url).read()
#     # print len(response)
#     # try:
#     #     img_url = re.findall(r'"url":"(.+?)"',response)[0]
#     #     print save_img(img_url)
#     # except:
#     #     print 'failed'

#     return HttpResponse('ok')
#---------------------------------
def get_g_hot(index,desc):
    reg_hot   = r'%d:{(.+?)}' % (index)
    one_dq    = re.findall(reg_hot, desc)[0]
    one_desc  = re.findall(r'0:"(.+?)"', one_dq)[0]
    one_query = re.findall(r'1:"(.+?)"', one_dq)[0]
    return one_desc.decode('utf8'),one_query.decode('utf8')

def get_today_bing_story():
    try:
        bingmsg = {'status':'success'}
        html    = urllib2.urlopen('http://cn.bing.com/cnhpm').read()
        title   = re.findall(r'<a .+?h="ID=SERP,5004.1">([\x00-\xff].*?)</a>',html)[0]
        bingmsg['title'] = title.decode('utf8')
        html    = urllib2.urlopen('http://cn.bing.com').read()
        imgurl = re.findall(r"g_img={url:'(.+?)'",html)[0]
        bingmsg['imgurl'] = imgurl
        desc    = re.findall(r"g_hot=(.+?);;",html)[0]
        for i in xrange(1,5):
            bingmsg[i] = get_g_hot(i,desc)
        return bingmsg
    except:
        return {'status':'failed'}

def save_img(img_url):
    try:
        img_name = img_url[img_url.rindex('/')+1:]
        img_data = urllib2.urlopen(img_url).read()
        img_fuffix = img_name[img_name.rindex('.'):]


        name = os.path.join('bing',uuid.uuid1().hex + img_fuffix).replace('\\','/')
        ret, err = qiniu.io.put(uptoken, name, img_data)
        if err is not None:
            print err
            return 'error',''
        #储存在七牛中的url
        qiniuurl = 'http://'+QINIU_BUCKET_NAME+'.qiniudn.com/'+name

        return 'success',qiniuurl
    except:
        return 'error',''


def bingindex(request):
    device  = get_user_device(request)
    template = 'photo/bingindex.html' if device == 'MOBILE' else 'photo/bingindex.html'

    tnow  = datetime.datetime.now()
    try:
        bing  = BingWallPaper.objects.filter(imgdate__gt = tnow).order_by('-imgdate')[0]
        return render_to_response(template, {'bingwallpaper':bing},
                              context_instance=RequestContext(request))
    except:
        tmid  = datetime.datetime(tnow.year, tnow.month, tnow.day) + datetime.timedelta(1)
        bingmsg = get_today_bing_story()
        if bingmsg['status'] == 'success':
            status, qiniuurl = save_img(bingmsg['imgurl'])
            bing = BingWallPaper(
                imgurl = bingmsg['imgurl'],
                desc1 = bingmsg[1][0],
                query1 = bingmsg[1][1],
                desc2 = bingmsg[2][0],
                query2 = bingmsg[2][1],
                desc3 = bingmsg[3][0],
                query3 = bingmsg[3][1],
                desc4 = bingmsg[4][0],
                query4 = bingmsg[4][1],
                title = bingmsg['title'],
                imgdate = tmid,
                qiniuimgurl = qiniuurl,
                )
            bing.save()
            return render_to_response(template, {'bingwallpaper':bing},
                              context_instance=RequestContext(request))
        return Http404
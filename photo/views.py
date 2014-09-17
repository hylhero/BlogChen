from django.shortcuts import render
from django.http.response import HttpResponse

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

def save_img(img_url):
    try:
        img_name = img_url[img_url.rindex('/')+1:]
        img_data = urllib2.urlopen(img_url).read()
        img_fuffix = img_name[img_name.rindex('.'):]

        todaytime = datetime.datetime.now().strftime('%Y%m%d')

        name = os.path.join('bing',uuid.uuid1().hex + img_fuffix).replace('\\','/')
        ret, err = qiniu.io.put(uptoken, name, img_data)
        if err is not None:
            print err
            return 'error',todaytime,'',''
        url = 'http://'+QINIU_BUCKET_NAME+'.qiniudn.com/'+name
        return 'success',todaytime,img_name,url
    except:
        return 'error',todaytime,'',''


def savebing(request):
    url = 'http://cn.bing.com'
    try:
        html = urllib2.urlopen(url).read()
        img_url = re.findall(r"g_img={url:'(.+?)'",html)[0]
        print save_img(img_url)
    except:
        print 'failed'
    # num = 1
    # tn = time.time()
    # url = 'http://cn.bing.com/HPImageArchive.aspx?format=js&idx=%d&n=1&nc=%d&pid=hp&scope=web&FORM=QBRE&video=1'%(num,int(tn))
    # response = urllib2.urlopen(url).read()
    # print len(response)
    # try:
    #     img_url = re.findall(r'"url":"(.+?)"',response)[0]
    #     print save_img(img_url)
    # except:
    #     print 'failed'

    return HttpResponse('ok')
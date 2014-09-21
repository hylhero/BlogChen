#-*- coding:utf-8 -*-

from django.db import models

import datetime

class BingWallPaper(models.Model):
    imgurl     = models.URLField(u'图片url')
    desc1      = models.CharField(u'描述1',max_length=60)
    query1     = models.CharField(u'查询1',max_length=60)
    desc2      = models.CharField(u'描述2',max_length=60)
    query2     = models.CharField(u'查询2',max_length=60)
    desc3      = models.CharField(u'描述3',max_length=60)
    query3     = models.CharField(u'查询3',max_length=60)
    desc4      = models.CharField(u'描述4',max_length=60)
    query4     = models.CharField(u'查询4',max_length=60)
    title      = models.CharField(u'标题', max_length=30)
    imgdate    = models.DateTimeField(u'图片时间', editable=False)
    qiniuimgurl= models.URLField(u'七牛URL')

    def __unicode__(self):
        return self.title
    class Meta:
        ordering            = ['-imgdate']
        db_table            = 'photo_bingwallpaper'
        verbose_name        = u'必应壁纸'
        verbose_name_plural = u'必应壁纸'

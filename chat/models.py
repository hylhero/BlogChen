#-*- coding:utf-8 -*-
from django.db import models


class ChatModel(models.Model):
    user = models.CharField(u'用户', max_length=30)
    time = models.DateTimeField(u'时间')
    msg = models.TextField(u'信息')
    ip = models.IPAddressField(u'IP')

    class Meta:
        db_table = 'chat'
        ordering = ['-time']
        verbose_name = u'聊天'
        verbose_name_plural = u'聊天'

    def __unicode__(self):
        return self.user

# -*- coding:utf-8 -*-

from django import template
from django.utils import timezone
import datetime


register = template.Library()

@register.tag
def shortname(namestr,maxl=16):
    # return blog.replace('i','I')
    if len(namestr) > maxl :
        return namestr[:13] + '...'
    return namestr
register.filter('shortname',shortname)

@register.tag
def formattime(pubtime):
    # return blog.replace('i','I')
    timenow         = timezone.now()
    delta           = timenow - pubtime
    delta_year      = delta.days/365
    delta_mounth    = (delta.days - delta_year*356)/30
    delta_days      = (delta.days - delta_year*356 - delta_mounth*30)
    delta_hours     = delta.seconds/3600
    delta_minutes   = (delta.seconds - delta_hours*3600)/60
    delta_seconds   = (delta.seconds - delta_hours*3600 - delta_minutes*60)

    if pubtime.year < timenow.year:
        return str(pubtime.year) + u'年' + str(pubtime.month) + u'月' + str(pubtime.day) + u'日'
        # return pubtime.strftime('%Y-%m-%d')
    elif pubtime.month < timenow.month or pubtime.day < timenow.day:
        return str(pubtime.month) + u'月' + str(pubtime.day) + u'日'
        # return pubtime.strftime('%m-%d %H:%I')
    elif delta_hours:
        return str(delta_hours) + u'小时前'
    elif delta_minutes:
        return str(delta_minutes) + u'分钟前'
    elif delta_seconds:
        return str(delta_seconds) + u'秒钟前'

register.filter('formattime',formattime)

from django.utils.safestring import mark_safe

@register.tag
def shortblog(content):
    # return blog.replace('i','I')
    line = 0
    i = 0
    while i < len(content):
        if line == 10:
            html = content[0:i]
            html = addtags(html)
            return mark_safe(html)
        if content[i] == '\n':
            line += 1
            i += 1
            continue
        if content[i] == '<' and content[i:i+4] == '</p>':
            line += 1
            i += 4
            continue
        if content[i:i+4] == '<img':
            line = 10
            while content[i] != '>':
                i += 1
        i += 1
    return mark_safe(content)
register.filter('shortblog',shortblog)

def addtags(html):
    tags = []
    i = 0
    while i < len(html):
        if html[i] == '<' and html[i+1] != '/' and html[i+1] != '!':
            i += 1
            b = i
            while html[i] != ' ' and html[i] != '>':
                i += 1
            tag = html[b:i]
            if tag in ['img','br/']:
                continue
            # print 'add',i,'   ',tag
            tags.append(tag)
        if html[i:i+2] == '</':
            i = i+2
            b = i
            while html[i] != '>':
                i += 1
            tag = html[b:i]
            # print 'mod',i,'   ',tag
            if tags[len(tags)-1] == tag:
                tags.pop(len(tags)-1)
        i += 1
    # print tags
    for i in xrange(len(tags)-1,-1,-1):
        html = html + '</'+tags[i]+'>\n'
    # print html
    return html
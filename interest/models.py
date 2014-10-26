# -*- coding: utf-8 -*-
from django.db import models
from photo.QiniuStorage import QiniuStorage


class MovieStyle(models.Model):
    name = models.CharField(u'电影类型', max_length=10)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'interest_moviestyle'
        verbose_name = u'电影类型'
        verbose_name_plural = u'电影类型'


class Actor(models.Model):
    ACTOR_OR_DIRECTOR = (
        ('A', u'演员'),
        ('D', u'导演'),
    )
    name = models.CharField(u'姓名', max_length=30)
    aord = models.CharField(u'导演或演员', max_length=1, choices=ACTOR_OR_DIRECTOR, default='A')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'interest_actor'
        verbose_name = u'电影演员'
        verbose_name_plural = u'电影演员'


class Area(models.Model):
    name = models.CharField(u'地区', max_length=10)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'interest_area'
        verbose_name = u'电影地区'
        verbose_name_plural = u'电影地区'


class Movie(models.Model):
    name = models.CharField(u'电影名', max_length=30)
    style = models.ManyToManyField(MovieStyle, blank=False, verbose_name=u'类型')
    area = models.ForeignKey(Area, null=False, verbose_name=u'地区')
    direct = models.ForeignKey(Actor, verbose_name=u'导演', related_name=u'导演')
    actors = models.ManyToManyField(Actor, verbose_name=u'演员', related_name=u'演员')
    info = models.TextField(u'简介')
    img = models.ImageField(upload_to='movies', verbose_name=u'海报', storage=QiniuStorage(folder='movies/'))
    releasedate = models.DateTimeField(u'上映时间')
    createdate = models.DateTimeField(u'上传时间', auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'interest_movie'
        verbose_name = u'电影'
        verbose_name_plural = u'电影'


class Book(models.Model):
    name = models.CharField(u'书名', max_length=30)
    createdate = models.DateTimeField(u'上传时间', auto_now_add=True, editable=False)
    img = models.ImageField(upload_to='books', verbose_name=u'封面', storage=QiniuStorage(folder='books/'))
    info = models.TextField(u'信息')
    burl = models.URLField(u'链接', blank=True, null=True)

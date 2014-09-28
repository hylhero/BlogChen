# -*- coding: utf-8 -*-
from django.db import models
from photo.QiniuStorage import QiniuStorage
# Create your models here.

class MovieStyleModel(models.Model):
    name    = models.CharField(u'电影类型', max_length=10)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering            = ['name']
        db_table            = 'interest_moviestyle'
        verbose_name        = u'电影类型'
        verbose_name_plural = u'电影类型'

class ActorModel(models.Model):
    name    = models.CharField(u'演员名', max_length=30)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering            = ['name']
        db_table            = 'interest_actor'
        verbose_name        = u'演员名'
        verbose_name_plural = u'演员名'

class AreaModel(models.Model):
    name    = models.CharField(u'地区', max_length=10)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering            = ['name']
        db_table            = 'interest_area'
        verbose_name        = u'地区'
        verbose_name_plural = u'地区'

class MovieModel(models.Model):
    name    = models.CharField(u'电影名', max_length=30)
    style   = models.ManyToManyField(MovieStyleModel, blank=False, verbose_name=u'类型')
    area    = models.ForeignKey(AreaModel, null=False, verbose_name=u'地区')
    direct  = models.ForeignKey(ActorModel, null=False, verbose_name=u'导演')
    actors  = models.ManyToManyField(ActorModel, blank=False, verbose_name=u'演员')
    info    = models.TextField(u'简介')
    img     = models.ImageField(upload_to='movies',verbose_name=u'海报',storage=QiniuStorage(folder='movies/'))
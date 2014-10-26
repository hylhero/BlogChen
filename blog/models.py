#!/usr/bin/env python
#-*- coding:utf-8 -*-
from django.db import models
from DjangoUeditor.models import UEditorField
import datetime
import os
from utils import get_ip_location


class Tag(models.Model):
    tag_name = models.CharField(u'名称', max_length=30)

    def __unicode__(self):
        return self.tag_name

    class Meta:
        ordering = ['tag_name']
        db_table = 'blog_Tag'
        verbose_name = u'标签'
        verbose_name_plural = u'标签'


class Category(models.Model):      # 分类
    category_name = models.CharField(u'名称', max_length=30)

    def __unicode__(self):
        return self.category_name

    class Meta:
        ordering = ['category_name']
        db_table = 'blog_Category'
        verbose_name = u'分类'
        verbose_name_plural = u'分类'


class User(models.Model):  # 用户
    USER_SEX = (
        ('M', u'男'),
        ('F', u'女'),
    )

    name = models.CharField(u'用户名', max_length=30)
    email = models.EmailField(u'邮箱', blank=True)
    website = models.URLField(u'博客网址', blank=True)
    photo = models.CharField(u'照片', max_length=255, null=True, blank=True, default='head.png')
    sex = models.CharField(u'性别', max_length=1, choices=USER_SEX, default='M')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'blog_User'
        verbose_name = u'用户'
        verbose_name_plural = u'用户'


class Blog(models.Model):  # 博文
    title = models.CharField(u'标题', max_length=200)
    publish_time = models.DateTimeField(u'发表时间', editable=False)
    update_time = models.DateTimeField(u'修改时间', editable=False)
    content = UEditorField(u'正文', width=1000, height=300, toolbars='full', imagePath='images/', filePath='files/')
    author = models.ForeignKey(User, null=True, blank=True, default=None, verbose_name=u'作者')
    read_num = models.IntegerField(u'阅读量', default=0, editable=False)
    comment_num = models.IntegerField(u'评论数', default=0, editable=False)
    category = models.ForeignKey(Category, verbose_name=u'分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=u'标签')

    def save(self, *args, **kwargs):
        if not self.id:
            self.publish_time = datetime.datetime.today()
        self.update_time = datetime.datetime.today()
        return super(Blog, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-publish_time']
        db_table = 'blog_Blog'
        verbose_name = u'博文'
        verbose_name_plural = u'博文'


class Link(models.Model):  # 链接
    site_name = models.CharField(u'连接名', max_length=30)
    site_url = models.URLField(u'地址', blank=False)
    site_description = models.CharField(u'描述', max_length=50)

    def __unicode__(self):
        return self.site_name

    class Meta:
        ordering = ['site_name']
        db_table = 'blog_Link'
        verbose_name = u'链接'
        verbose_name_plural = u'链接'


class Comment(models.Model):  # 评论
    pre_com = models.ForeignKey('self', null=True, blank=True, default=None, verbose_name=u'父级评论')
    user = models.ForeignKey(User, verbose_name=u'用户')
    blog = models.ForeignKey(Blog, verbose_name=u'文章')
    content = models.TextField(u'评论内容')
    comment_time = models.DateTimeField(u'评论时间')

    def __unicode__(self):
        return unicode(self.id)

    class Meta:
        ordering = ['-comment_time']
        db_table = 'blog_comment'
        verbose_name = u'评论'
        verbose_name_plural = u'评论'


class UploadFileModel(models.Model):  # 上传文件
    filename = models.CharField(u'文件名', max_length=128)
    filetype = models.CharField(u'类型', max_length=20)
    filepath = models.TextField(u'文件路径')
    filesize = models.IntegerField(u'大小(字节)')
    uploaddate = models.DateTimeField(u'上传时间', editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.uploaddate = datetime.datetime.today()
        return super(UploadFileModel, self).save(*args, **kwargs)

    def delete(self, using=None):
        if self.id:
            fpath = './upload' + self.filepath
            if os.path.isfile(fpath):
                os.remove(fpath)
            return super(UploadFileModel, self).delete(using)

    class Meta:
        ordering = ['-uploaddate']
        db_table = 'blog_uploadfile'
        verbose_name = u'文件'
        verbose_name_plural = u'文件'


class FeedBackModel(models.Model):  # 反馈意见
    username = models.CharField(u'昵称', max_length=36)
    useremail = models.EmailField(u'邮箱')
    suggestion = models.TextField(u'反馈意见')
    feedback_time = models.DateTimeField(u'反馈时间', editable=False, auto_now_add=True)

    class Meta:
        ordering = ['-feedback_time']
        db_table = 'blog_feedback'
        verbose_name = u'反馈'
        verbose_name_plural = u'反馈'


class UserVisitFoot(models.Model):  # 用户访问记录
    userIP = models.IPAddressField(u'访问IP', unique=True)
    visitednum = models.IntegerField(u'访问次数', default=0)
    visitedpre = models.DateTimeField(u'上一次访问时间', editable=False)
    visitedlatest = models.DateTimeField(u'最近访问时间', editable=False, auto_now_add=True)
    address = models.CharField(u'归属地', max_length=60, default='')

    def save(self, *args, **kwargs):
        if not self.id:
            self.visitedpre = datetime.datetime.today()
            self.visitedlatest = datetime.datetime.today()
            self.visitednum = 1
        else:
            timenow = datetime.datetime.today()
            t = timenow.strftime('%Y-%m-%d')
            t = t.split('-')
            t = tuple(int(i) for i in tuple(t))
            midnight = datetime.datetime(*t)
            if self.visitedlatest < midnight:
                self.visitednum += 1
                self.visitedpre = self.visitedlatest
            self.visitedlatest = timenow
            if self.userIP and (self.address == '' or self.address == None):
                self.address = get_ip_location(self.userIP)

        return super(UserVisitFoot, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.userIP)

    class Meta:
        ordering = ['-visitedlatest', '-visitedpre', 'userIP']
        db_table = 'blog_uservisitfoot'
        verbose_name = u'足迹'
        verbose_name_plural = u'足迹'
